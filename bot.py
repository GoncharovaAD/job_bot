import asyncio
import os
import threading
from typing import List
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Bot
from telegram.constants import ParseMode

from config import (
    TRACKS, ADZUNA_APP_ID, ADZUNA_APP_KEY, 
    BOT_TOKEN, TELEGRAM_CHAT_ID,
    CHECK_INTERVAL_MINUTES, MAX_JOBS_PER_CHECK
)
from sources import get_all_sources, JobItem
from matching.profile import calculate_match_score, generate_dedup_hash, is_remote_job
from database import Database

# --- Встроенный веб-сервер для прохождения Port Scan на Render ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")
    
    def log_message(self, format, *args):
        # Отключаем спам-логи запросов в консоли
        pass

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    print(f"🌐 Health check server bound to port {port}")
    httpd.serve_forever()

# Запускаем фоновый веб-сервер сразу при импорте/старте модуля
threading.Thread(target=run_health_server, daemon=True).start()
# -----------------------------------------------------------------

COUNTRY_FLAGS = {
    "germany": "🇩🇪", "deutschland": "🇩🇪",
    "uk": "🇬🇧", "united kingdom": "🇬🇧", "england": "🇬🇧",
    "netherlands": "🇳🇱", "amsterdam": "🇳🇱",
    "france": "🇫🇷", "paris": "🇫🇷",
    "spain": "🇪🇸", "madrid": "🇪🇸", "barcelona": "🇪🇸",
    "austria": "🇦🇹", "vienna": "🇦🇹",
    "switzerland": "🇨🇭", "zurich": "🇨🇭",
    "poland": "🇵🇱", "warsaw": "🇵🇱",
    "italy": "🇮🇹", "rome": "🇮🇹",
    "sweden": "🇸🇪", "stockholm": "🇸🇪",
    "finland": "🇫🇮", "helsinki": "🇫🇮",
    "norway": "🇳🇴", "oslo": "🇳🇴"
}

def format_job_card(track_title: str, job: JobItem, score: int) -> str:
    """Формирует аккуратную карточку вакансии для Telegram в стиле Research-детекта."""
    clean_title = (
        job.title.replace("<b>", "")
        .replace("</b>", "")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    
    loc_lower = job.location.lower() if job.location else ""
    flag = "🇪🇺"
    for place, f in COUNTRY_FLAGS.items():
        if place in loc_lower:
            flag = f
            break
            
    if "remote" in loc_lower:
        location_str = f"{flag} Remote ({job.location})"
    else:
        location_str = f"{flag} Remote | {job.location}"

    raw_tags = job.tags if getattr(job, 'tags', None) else ["EU Remote"]
    cleaned_tags = []
    for t in raw_tags:
        clean_t = str(t).replace("'", "").replace('"', "").replace("[", "").replace("]", "")
        if clean_t.strip():
            cleaned_tags.append(clean_t.strip())
            
    tags_str = " · ".join(cleaned_tags[:3]) if cleaned_tags else "EU Remote"

    return (
        f"🎯 <b>{track_title}</b>\n\n"
        f"<b>{clean_title}</b>\n"
        f"<i>{job.company}</i> · <i>{tags_str}</i>\n"
        f"📍 {location_str}\n"
        f"🎯 Match {score}%\n\n"
        f"🔗 <a href='{job.url}'>Apply via {job.source_id.capitalize()}</a>"
    )

async def check_and_send_jobs(bot: Bot, db: Database):
    sources = get_all_sources(ADZUNA_APP_ID, ADZUNA_APP_KEY)
    sent_total = 0

    for track in TRACKS:
        track_title = getattr(track, 'name', getattr(track, 'title', 'Job Track'))
        print(f"\n=== Fetching for Track: {track_title} ===")
        track_jobs: List[JobItem] = []

        for source in sources:
            try:
                jobs = await source.fetch_jobs(track.search_keywords)
                print(f"[{source.name}] Found {len(jobs)} potential jobs")
                track_jobs.extend(jobs)
            except Exception as e:
                print(f"Error fetching from {source.name}: {e}")

        new_jobs_count = 0
        for job in track_jobs:
            if sent_total >= MAX_JOBS_PER_CHECK:
                print(f"⚠️ Достигнут лимит MAX_JOBS_PER_CHECK ({MAX_JOBS_PER_CHECK}).")
                return

            # 1. Строгая проверка на Fully Remote (и отсечение гибридов/офиса)
            if not is_remote_job(job):
                continue

            # 🚫 1.1. Исключаем США
            loc_lower = job.location.lower() if job.location else ""
            if any(us_word in loc_lower for us_word in ["united states", ", us", "usa", "america"]):
                continue

            # 2. Проверка дедупликации через базу
            dedup_hash = generate_dedup_hash(job)
            if db.is_duplicate(dedup_hash):
                continue

            # 3. Расчет скоринга по профилю "Technical Detective"
            score = calculate_match_score(job, track)
            if score < 60:
                continue

            card_text = format_job_card(track_title, job, score)
            
            try:
                await bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=card_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
                print(f"✅ [{track_title}] Отправлена: {job.title}")
                
                db.mark_seen(dedup_hash, job.source_id)
                new_jobs_count += 1
                sent_total += 1
                
                await asyncio.sleep(2)
            except Exception as e:
                print(f"❌ Ошибка отправки в Telegram: {e}")

        print(f"Finished {track_title}: {new_jobs_count} new unique jobs sent.")

    return sent_total

async def main():
    if not BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Ошибка: Укажи BOT_TOKEN и TELEGRAM_CHAT_ID в файле .env / config.py!")
        return

    bot = Bot(token=BOT_TOKEN)
    db = Database()

    print(f"🚀 JobStormBot v2.2 (Technical Detective Edition) запущен!")
    print(f"⚙️ Интервал: каждые {CHECK_INTERVAL_MINUTES} мин. | Лимит: {MAX_JOBS_PER_CHECK} вакансий/чек.\n")

    # Отслеживаем время отправки последнего сообщения (вакансии или статуса)
    last_sent_time = asyncio.get_event_loop().time()

    while True:
        try:
            print("⏰ Начинаем поисковую миссию...")
            
            # check_and_send_jobs должен возвращать количество отправленных вакансий
            sent_count = await check_and_send_jobs(bot, db)
            
            current_time = asyncio.get_event_loop().time()
            
            if sent_count > 0:
                last_sent_time = current_time
            else:
                # 86400 секунд = 24 часа
                if current_time - last_sent_time >= 86400:
                    status_message = (
                        "🕵️‍♂️ <b>Детективный отчет за сутки:</b>\n\n"
                        "За последние 24 часа новых подходящих вакансий не обнаружено. "
                        "Сканеры работают в штатном режиме, поиск продолжается! 🫡"
                    )
                    await bot.send_message(
                        chat_id=TELEGRAM_CHAT_ID,
                        text=status_message,
                        parse_mode=ParseMode.HTML
                    )
                    print("ℹ️ Отправлен суточный отчет об отсутствии вакансий.")
                    last_sent_time = current_time

        except Exception as e:
            print(f"💥 Ошибка во время цикла сбора: {e}")

        sleep_seconds = CHECK_INTERVAL_MINUTES * 60
        print(f"\n💤 Следующая проверка через {CHECK_INTERVAL_MINUTES} минут...")
        await asyncio.sleep(sleep_seconds)

if __name__ == "__main__":
    asyncio.run(main())
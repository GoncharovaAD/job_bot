import asyncio
from typing import List
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

def format_job_card(track_name: str, job: JobItem, score: int) -> str:
    """Формирует аккуратную карточку вакансии для Telegram."""
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

    tags_str = " · ".join([t for t in job.tags if t][:3]) if getattr(job, 'tags', None) else "EU Remote"

    return (
        f"🎯 <b>{track_name}</b>\n\n"
        f"<b>{clean_title}</b>\n"
        f"<i>{job.company}</i> · <i>{tags_str}</i>\n"
        f"📍 {location_str}\n"
        f"🎯 Match {score}%\n\n"
        f"🔗 <a href='{job.url}'>Apply via {job.source_id.capitalize()}</a>"
    )

async def check_and_send_jobs(bot: Bot, db: Database):
    sources = get_all_sources(ADZUNA_APP_ID, ADZUNA_APP_KEY)
    sent_total = 0

    # Исправлено: перебираем список TRACKS напрямую
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

            # 1. Жесткая проверка на Remote
            if not is_remote_job(job):
                continue

            # 2. Проверка на дубликат по компании и названию
            dedup_hash = generate_dedup_hash(job)
            if db.is_duplicate(dedup_hash):
                continue

            # 3. Расчет скоринга и проверка негативных слов
            score = calculate_match_score(job, track)
            if score == 0:
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
                
                await asyncio.sleep(2)  # Пауза между отправками
            except Exception as e:
                print(f"❌ Ошибка отправки в Telegram: {e}")

        print(f"Finished {track_title}: {new_jobs_count} new unique jobs sent.")

async def main():
    if not BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Ошибка: Укажи BOT_TOKEN и TELEGRAM_CHAT_ID в файле .env / config.py!")
        return

    bot = Bot(token=BOT_TOKEN)
    db = Database()

    print(f"🚀 JobStormBot v2.1 запущен!")
    print(f"⚙️ Интервал: каждые {CHECK_INTERVAL_MINUTES} мин. | Лимит: {MAX_JOBS_PER_CHECK} вакансий/чек.\n")

    while True:
        try:
            print("⏰ Начинаем проверку свежих вакансий...")
            await check_and_send_jobs(bot, db)
        except Exception as e:
            print(f"💥 Ошибка во время цикла сбора: {e}")

        sleep_seconds = CHECK_INTERVAL_MINUTES * 60
        print(f"\n💤 Следующая проверка через {CHECK_INTERVAL_MINUTES} минут...")
        await asyncio.sleep(sleep_seconds)

if __name__ == "__main__":
    asyncio.run(main())
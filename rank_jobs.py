import asyncio
from typing import List, Tuple
from config import TRACKS, ADZUNA_APP_ID, ADZUNA_APP_KEY
from sources import get_all_sources, JobItem
from matching.profile import calculate_match_score, is_remote_job, generate_dedup_hash

async def run_ranking(top_n: int = 20):
    print("🔎 Начинаем глубокий поиск и ранжирование всех вакансий...\n")
    sources = get_all_sources(ADZUNA_APP_ID, ADZUNA_APP_KEY)
    
    # Сюда сохраняем пары: (score, track_title, job_item)
    ranked_jobs: List[Tuple[int, str, JobItem]] = []
    seen_hashes = set()

    for track_id, track in TRACKS.items():
        print(f"📡 Опрос источников для трека: {track.title}...")
        track_jobs: List[JobItem] = []

        for source in sources:
            try:
                jobs = await source.fetch_jobs(track.keywords)
                track_jobs.extend(jobs)
            except Exception as e:
                print(f"❌ Ошибка [{source.name}]: {e}")

        print(f"   └─ Собрано {len(track_jobs)} потенциальных вакансий.")

        # Фильтрация и расчет скоринга
        for job in track_jobs:
            # 1. Проверка на Remote
            if not is_remote_job(job):
                continue

            # 2. Дедупликация в рамках одного прогона
            dedup_hash = generate_dedup_hash(job)
            if dedup_hash in seen_hashes:
                continue
            seen_hashes.add(dedup_hash)

            # 3. Расчет скоринга
            score = calculate_match_score(job, track)
            if score > 0:
                ranked_jobs.append((score, track.title, job))

    # Сортировка по убыванию % Match
    ranked_jobs.sort(key=lambda x: x[0], reverse=True)

    print("\n" + "=" * 60)
    print(f"🏆 ТОП-{min(top_n, len(ranked_jobs))} НАИБОЛЕЕ ПОДХОДЯЩИХ ВАКАНСИЙ (из {len(ranked_jobs)} отобранных)")
    print("=" * 60 + "\n")

    output_lines = []

    for idx, (score, track_title, job) in enumerate(ranked_jobs[:top_n], start=1):
        line = (
            f"{idx}. [{score}% Match] [{track_title}] {job.title}\n"
            f"   🏢 Компания: {job.company}\n"
            f"   📍 Локация: {job.location}\n"
            f"   🌐 Источник: {job.source_id.upper()}\n"
            f"   🔗 Ссылка: {job.url}\n"
            f"   ------------------------------------"
        )
        print(line)
        output_lines.append(line)

    if not ranked_jobs:
        print("😔 Подходящих вакансий с высоким Match Score не найдено.")

if __name__ == "__main__":
    # Запускаем ранжирование с выводом ТОП-20 результатов
    asyncio.run(run_ranking(top_n=20))
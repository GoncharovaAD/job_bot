import asyncio
from config import TRACKS, ADZUNA_APP_ID, ADZUNA_APP_KEY
from sources.remotive import RemotiveSource
from sources.jobicy import JobicySource
from sources.adzuna import AdzunaSource
from matching.profile import calculate_match_score, is_remote_job

async def debug_search():
    # Инициализируем источники с необходимыми параметрами
    sources = [
        ("remotive", RemotiveSource()),
        ("Jobicy", JobicySource()),
        ("adzuna", AdzunaSource(app_id=ADZUNA_APP_ID, app_key=ADZUNA_APP_KEY))
    ]

    for track in TRACKS:
        print(f"\n==========================================")
        print(f"🎯 ТРЕК: {track.name}")
        print(f"Запросы для API: {track.search_keywords}")
        print(f"==========================================")

        for source_name, source_inst in sources:
            print(f"\n📡 Запрос к источнику: [{source_name}]")
            try:
                # В зависимости от метода поиска в классе
                if hasattr(source_inst, 'fetch_jobs'):
                    jobs = await source_inst.fetch_jobs(track.search_keywords)
                elif hasattr(source_inst, 'get_jobs'):
                    jobs = await source_inst.get_jobs(track.search_keywords)
                elif hasattr(source_inst, 'search'):
                    jobs = await source_inst.search(track.search_keywords)
                else:
                    print(f"   └─ ❌ У объекта {source_name} не найден метод поиска")
                    continue

                print(f"   ├─ Ответ от {source_name}: получено {len(jobs)} вакансий.")
                
                for job in jobs[:3]:
                    remote_status = is_remote_job(job)
                    score = calculate_match_score(job, track)
                    print(f"   ├─ 📄 '{job.title}' | Компания: {job.company}")
                    print(f"   │    └─ Remote: {remote_status} | Score: {score}%")
            except Exception as e:
                print(f"   └─ ❌ Ошибка при запросе: {e}")

if __name__ == "__main__":
    asyncio.run(debug_search())


data = response.json()
print(f"Тип данных: {type(data)}, Содержимое: {data[:2] if isinstance(data, list) else data}")
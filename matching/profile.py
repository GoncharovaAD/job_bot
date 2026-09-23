import hashlib
from typing import List
from sources import JobItem

def generate_dedup_hash(job: JobItem) -> str:
    """Генерация уникального хэша вакансии для дедупликации."""
    raw_string = f"{job.company.strip().lower()}_{job.title.strip().lower()}"
    return hashlib.md5(raw_string.encode('utf-8')).hexdigest()

def is_remote_job(job: JobItem) -> bool:
    """Проверка, является ли вакансия удаленной."""
    loc_lower = job.location.lower() if job.location else ""
    title_lower = job.title.lower() if job.title else ""
    
    remote_keywords = ["remote", "worldwide", "anywhere", "distributed", "wfh", "eu remote"]
    
    is_loc_remote = any(kw in loc_lower for kw in remote_keywords)
    is_title_remote = any(kw in title_lower for kw in remote_keywords)
    
    return is_loc_remote or is_title_remote

def calculate_match_score(job: JobItem, track) -> int:
    """Расчет соответствия вакансии треку с жестким порогом качества."""
    title_lower = job.title.lower() if job.title else ""
    
    # Собираем всю инфо-строку (название + теги) для проверки стоп-слов
    job_tags_str = " ".join([str(t).lower() for t in getattr(job, 'tags', [])])
    full_job_info = f"{title_lower} {job_tags_str}"
    
    # 1. Проверка negative_keywords из конфигурации трека
    negative_keywords = getattr(track, 'negative_keywords', [])
    for neg in negative_keywords:
        if neg.lower() in full_job_info:
            return 0  # Сразу отсекаем

    track_title = getattr(track, 'title', getattr(track, 'name', getattr(track, 'query', '')))
    track_title_lower = track_title.lower() if track_title else ""
    
    # 2. Проверка на уровень для джун-треков
    if "junior" in track_title_lower or "jun" in track_title_lower:
        forbidden_levels = [
            "senior", "sr.", "staff", "lead", "principal", 
            "mid", "middle", "experienced", "manager", "director"
        ]
        if any(level in full_job_info for level in forbidden_levels):
            return 0  

    # 3. Умный расчет скоринга (стартовая база ниже порога отправки 75)
    score = 40  
    
    keywords = getattr(track, 'search_keywords', [])
    matched_keywords = sum(1 for kw in keywords if kw.lower() in title_lower)
    
    if matched_keywords > 0:
        score += matched_keywords * 20
        
    return min(score, 100)
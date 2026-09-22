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
    """Расчет соответствия вакансии треку."""
    title_lower = job.title.lower() if job.title else ""
    
    # Универсально получаем название трека (проверяем title, name или query)
    track_title = getattr(track, 'title', getattr(track, 'name', getattr(track, 'query', '')))
    track_title_lower = track_title.lower() if track_title else ""
    
    # Жестко отсекаем Senior / Staff / Lead / Mid для джун-треков
    if "junior" in track_title_lower or "jun" in track_title_lower:
        forbidden_levels = ["senior", "sr.", "staff", "lead", "principal", "mid", "middle"]
        if any(level in title_lower for level in forbidden_levels):
            return 0  # Сразу отсекаем

    score = 50  # Базовый скор для прошедших фильтр
    
    # Простая проверка по ключевым словам трека
    keywords = getattr(track, 'search_keywords', [])
    matched_keywords = sum(1 for kw in keywords if kw.lower() in title_lower)
    
    if matched_keywords > 0:
        score += min(matched_keywords * 15, 40)
        
    return min(score, 100)
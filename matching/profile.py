import hashlib
from typing import List
from sources import JobItem

def generate_dedup_hash(job: JobItem) -> str:
    """Генерация уникального хэша вакансии для дедупликации."""
    raw_string = f"{job.company.strip().lower()}_{job.title.strip().lower()}"
    return hashlib.md5(raw_string.encode('utf-8')).hexdigest()

def is_remote_job(job: JobItem) -> bool:
    """Мягкая и гибкая проверка на удаленку (EU / Worldwide / Remote)."""
    loc_lower = job.location.lower() if job.location else ""
    title_lower = job.title.lower() if job.title else ""
    
    # Жесткие стоп-сигналы для явного офиса
    office_signals = ["on-site only", "office only", "must be in office", "relocation required to office"]
    if any(sig in loc_lower for sig in office_signals):
        return False

    # Если в локации или названии есть намек на удаленку, разрешаем
    remote_keywords = [
        "remote", "worldwide", "anywhere", "distributed", "wfh", 
        "eu", "europe", "germany", "netherlands", "spain", "poland", "global", "home"
    ]
    
    # Если локация пустая у надежных платформ — тоже даем шанс
    if not loc_lower:
        return True

    is_loc_remote = any(kw in loc_lower for kw in remote_keywords)
    is_title_remote = any(kw in title_lower for kw in remote_keywords)
    
    return is_loc_remote or is_title_remote

def calculate_match_score(job: JobItem, track) -> int:
    """
    Интеллектуальный скоринг сбалансированного типа.
    """
    title_lower = job.title.lower() if job.title else ""
    job_tags_str = " ".join([str(t).lower() for t in getattr(job, 'tags', [])])
    full_job_info = f"{title_lower} {job_tags_str}"
    
    # 1. Негативные ключевые слова трека
    negative_keywords = getattr(track, 'negative_keywords', [])
    for neg in negative_keywords:
        if neg.lower() in full_job_info:
            return 0  

    # 2. Токсичные флаги
    toxic_flags = ["strict working hours", "screen monitoring"]
    if any(flag in full_job_info for flag in toxic_flags):
        return 0

    track_title = getattr(track, 'title', getattr(track, 'name', getattr(track, 'query', '')))
    track_title_lower = track_title.lower() if track_title else ""
    
    if "junior" in track_title_lower or "jun" in track_title_lower:
        forbidden_levels = ["senior", "sr.", "staff", "lead", "principal", "architect"]
        if any(level in full_job_info for level in forbidden_levels):
            return 0  

    # Базовый старт выше, чтобы хорошие вакансии пробивали порог
    score = 40  
    
    # Детективные и аналитические сигналы
    detective_signals = [
        "research", "investigate", "troubleshoot", "debug", "analyze", 
        "verify", "root cause", "trace", "api", "problem"
    ]
    detective_matches = sum(1 for sig in detective_signals if sig in full_job_info)
    score += detective_matches * 12

    # Технические маркеры
    tech_signals = [
        "python", "sql", "postgresql", "api", "git", "automation", 
        "meteorology", "climate", "science", "data", "documentation", "writer"
    ]
    tech_matches = sum(1 for ts in tech_signals if ts in full_job_info)
    score += tech_matches * 8

    # Совпадение по ключевым словам трека
    keywords = getattr(track, 'search_keywords', [])
    matched_keywords = sum(1 for kw in keywords if kw.lower() in title_lower)
    if matched_keywords > 0:
        score += matched_keywords * 15
        
    return min(score, 100)
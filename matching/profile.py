import hashlib
from typing import List
from sources import JobItem

def generate_dedup_hash(job: JobItem) -> str:
    """Генерация уникального хэша вакансии для дедупликации."""
    raw_string = f"{job.company.strip().lower()}_{job.title.strip().lower()}"
    return hashlib.md5(raw_string.encode('utf-8')).hexdigest()

def is_remote_job(job: JobItem) -> bool:
    """Проверка, является ли вакансия строго удаленной (никаких гибридов)."""
    loc_lower = job.location.lower() if job.location else ""
    title_lower = job.title.lower() if job.title else ""
    
    # Жесткий стоп-лист для гибридов и офисов
    hybrid_office_signals = [
        "hybrid", "office", "onsite", "on-site", "relocation", 
        "commuting", "days per week in office", "days a month in office"
    ]
    if any(sig in loc_lower for sig in hybrid_office_signals) or any(sig in title_lower for sig in hybrid_office_signals):
        return False

    remote_keywords = ["remote", "worldwide", "anywhere", "distributed", "wfh", "eu remote", "global"]
    is_loc_remote = any(kw in loc_lower for kw in remote_keywords)
    is_title_remote = any(kw in title_lower for kw in remote_keywords)
    
    return is_loc_remote or is_title_remote

def calculate_match_score(job: JobItem, track) -> int:
    """
    Интеллектуальный скоринг по принципу 'Technical Detective'.
    Ищет суть задач: research, troubleshooting, debug, science, python, autonomy.
    """
    title_lower = job.title.lower() if job.title else ""
    
    # Собираем контекст для глубокого анализа
    job_tags_str = " ".join([str(t).lower() for t in getattr(job, 'tags', [])])
    full_job_info = f"{title_lower} {job_tags_str}"
    
    # 1. Проверяем негативные ключевые слова трека
    negative_keywords = getattr(track, 'negative_keywords', [])
    for neg in negative_keywords:
        if neg.lower() in full_job_info:
            return 0  # Сразу отклоняем

    # 2. Красные флаги токсичной среды / микроменеджмента / жесткого контроля
    toxic_flags = [
        "time tracking", "activity monitoring", "screen monitoring", 
        "strict working hours", "micromanagement"
    ]
    if any(flag in full_job_info for flag in toxic_flags):
        return 0

    track_title = getattr(track, 'title', getattr(track, 'name', getattr(track, 'query', '')))
    track_title_lower = track_title.lower() if track_title else ""
    
    # 3. Отсев старших грейдов для джун-треков
    if "junior" in track_title_lower or "jun" in track_title_lower:
        forbidden_levels = ["senior", "sr.", "staff", "lead", "principal", "mid", "middle", "experienced"]
        if any(level in full_job_info for level in forbidden_levels):
            return 0  

    # 4. Система весов «Технического Детектива» (Task-Similarity вместо Title-Similarity)
    score = 30  # Базовая база ниже порога отправки (75)
    
    # Сигналы расследования и отладки (высший приоритет)
    detective_signals = [
        "research", "investigate", "troubleshoot", "debug", "analyze", 
        "verify", "root cause", "trace", "reverse-engineer", "problem solving"
    ]
    detective_matches = sum(1 for sig in detective_signals if sig in full_job_info)
    score += detective_matches * 15

    # Технические маркеры (Python, SQL, API, Git, Science)
    tech_signals = [
        "python", "sql", "postgresql", "api", "git", "automation", 
        "meteorology", "climate", "science", "data", "rag", "knowledge"
    ]
    tech_matches = sum(1 for ts in tech_signals if ts in full_job_info)
    score += tech_matches * 10

    # Совпадение ключевых слов трека
    keywords = getattr(track, 'search_keywords', [])
    matched_keywords = sum(1 for kw in keywords if kw.lower() in title_lower)
    if matched_keywords > 0:
        score += matched_keywords * 10
        
    return min(score, 100)
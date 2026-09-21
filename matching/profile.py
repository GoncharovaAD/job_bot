import re
from sources.base import JobItem
from config import TrackConfig, TECH_STACK_KEYWORDS

# Языки, которые НЕ подходят (нужен только английский)
LANGUAGE_NOISE_KEYWORDS = [
    "korean", "japanese", "chinese", "german", "deutsch", "french", 
    "spanish", "italian", "dutch", "polish", "portuguese"
]

# Нежелательные роли и шум
TITLE_NOISE_KEYWORDS = [
    "support", "customer support", "helpdesk", "customer service",
    "shopify", "wordpress", "copywriter", "marketing writer", 
    "sales manager", "sales executive", "account manager", "recruiter", "hr manager",
    "inside sales", "social media", "concept/copy"
]

# Проверка на соответствие уровню (если трек Junior, отсекаем Senior/Staff/Lead/Mid)
title_lower = job.title.lower()
if "junior" in track.title.lower() or "jun" in track.title.lower():
    forbidden_levels = ["senior", "sr.", "staff", "lead", "principal", "mid", "middle"]
    if any(level in title_lower for level in forbidden_levels):
            # Пропускаем эту вакансию, так как она выше уровня Junior
        continue


def is_remote_job(job: JobItem) -> bool:
    if job.source_id in ["remotive", "jobicy"]:
        return True

    full_text = f"{job.title} {job.location} {job.description}".lower()
    remote_terms = ["remote", "work from home", "anywhere", "telecommute", "удаленка", "homeoffice", "flex"]
    
    return any(term in full_text for term in remote_terms)

def calculate_match_score(job: JobItem, track: TrackConfig) -> int:
    title_lower = job.title.lower()
    text_lower = f"{job.title} {job.description}".lower()

    # 1. Полностью отключаем Arbeitnow (немецкие вакансии)
    if job.source_id == "arbeitnow":
        return 0

    # 2. Исключаем вакансии с неанглийскими языками в названии (Korean, German и т.д.)
    if any(lang in title_lower for lang in LANGUAGE_NOISE_KEYWORDS):
        return 0

    # 3. Отсекаем Support, Sales и коммерческий шум
    if any(noise in title_lower for noise in TITLE_NOISE_KEYWORDS):
        return 0

    # 4. Если это "Software Engineer/Developer" без упоминания Docs — берем только Junior
    if "software engineer" in title_lower or "developer" in title_lower:
        is_docs_role = any(d in title_lower for d in ["doc", "docs", "writer", "documentation"])
        is_junior_role = any(j in title_lower or j in text_lower for j in ["junior", "intern", "trainee", "entry level"])
        
        if not is_docs_role and not is_junior_role and track.name != "WEATHER & CLIMATE TECH":
            return 0

    # 5. Проверяем негативные ключевые слова конкретного трека
    for neg_kw in track.negative_keywords:
        if neg_kw.lower() in title_lower:
            return 0

    # 6. Расчет соответствия
    exact_matches = sum(1 for kw in track.keywords if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text_lower))
    search_title_matches = sum(1 for skw in track.search_keywords if skw.lower() in title_lower)
    search_text_matches = sum(1 for skw in track.search_keywords if skw.lower() in text_lower)
    stack_matches = sum(1 for tech in TECH_STACK_KEYWORDS if tech in text_lower)

    if search_title_matches == 0 and exact_matches == 0 and search_text_matches == 0:
        return 0

    score = 55
    score += search_title_matches * 15
    score += exact_matches * 10
    score += stack_matches * 2

    if score < 60:
        return 0

    return min(score, 98)

def generate_dedup_hash(job: JobItem) -> str:
    clean_title = re.sub(r'[^a-zA-Z0-9]', '', job.title.lower())
    clean_company = re.sub(r'[^a-zA-Z0-9]', '', job.company.lower())
    return f"{clean_company}:{clean_title}"
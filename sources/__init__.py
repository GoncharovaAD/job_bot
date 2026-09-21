from typing import List
from .base import BaseSource, JobItem
from .arbeitnow import ArbeitnowSource
from .remotive import RemotiveSource
from .adzuna import AdzunaSource
from .jobicy import JobicySource

def get_all_sources(adzuna_id: str = "", adzuna_key: str = "") -> List[BaseSource]:
    """Возвращает список всех активных источников вакансий."""
    sources: List[BaseSource] = [
        ArbeitnowSource(),
        RemotiveSource(),
        JobicySource()
    ]
    
    # Добавляем Adzuna только если переданы API ключи
    if adzuna_id and adzuna_key:
        sources.append(AdzunaSource(app_id=adzuna_id, app_key=adzuna_key))
        
    return sources

__all__ = ["get_all_sources", "JobItem", "BaseSource"]
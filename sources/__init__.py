from typing import List
from .base import BaseSource, JobItem
from .arbeitnow import ArbeitnowSource
from .remotive import RemotiveSource
from .adzuna import AdzunaSource
from .jobicy import JobicySource
from .remoteok import RemoteOKSource
from .himalayas import HimalayasSource

def get_all_sources(adzuna_id: str = "", adzuna_key: str = ""):
    sources = [
        ArbeitnowSource(),
        RemotiveSource(),
        AdzunaSource(),
        JobicySource(),
        RemoteOKSource(),
        HimalayasSource(),
    ]
    
    # Добавляем Adzuna только если ключи действительно переданы
    if adzuna_id and adzuna_key:
        sources.append(AdzunaSource(app_id=adzuna_id, app_key=adzuna_key))
        
    return sources

__all__ = ["get_all_sources", "JobItem", "BaseSource"]
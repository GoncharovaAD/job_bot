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
        JobicySource(),
        RemoteOKSource(),
        HimalayasSource(),
    ]
    
    # Добавляем Adzuna только при наличии обоих ключей
    if adzuna_id and adzuna_key:
        try:
            sources.append(AdzunaSource(app_id=adzuna_id, app_key=adzuna_key))
        except Exception as e:
            print(f"⚠️ Не удалось подключить Adzuna: {e}")
        
    return sources

__all__ = ["get_all_sources", "JobItem", "BaseSource"]
from typing import List
from .base import BaseSource, JobItem
from .arbeitnow import ArbeitnowSource
from .remotive import RemotiveSource
from .adzuna import AdzunaSource

def get_all_sources(adzuna_id: str = "", adzuna_key: str = "") -> List[BaseSource]:
    sources = [
        ArbeitnowSource(),
        RemotiveSource()
    ]
    if adzuna_id and adzuna_key:
        sources.append(AdzunaSource(app_id=adzuna_id, app_key=adzuna_key))
    return sources
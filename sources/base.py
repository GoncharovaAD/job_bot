from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

@dataclass
class JobItem:
    source_id: str      # e.g. "arbeitnow", "remotive", "jobicy"
    original_id: str    # ID вакансии в источнике
    title: str
    company: str
    location: str
    url: str
    description: str
    tags: List[str]

class BaseSource(ABC):
    name: str

    @abstractmethod
    async def fetch_jobs(self, keywords: List[str]) -> List[JobItem]:
        """Получить список вакансий по ключам"""
        pass
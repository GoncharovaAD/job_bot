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

class BaseSource:
    def __init__(self, *args, **kwargs):
        # Универсальный перехват любых аргументов из super().__init__(...)
        if args:
            self.name = str(args[0])
        elif "name" in kwargs:
            self.name = str(kwargs["name"])
        else:
            # Если имя не передано, берем имя класса (например, "HimalayasSource" -> "himalayas")
            self.name = self.__class__.__name__.lower().replace("source", "")
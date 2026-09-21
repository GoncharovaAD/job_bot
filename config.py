import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Ключи API и Telegram (с поддержкой разных имен импорта)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", os.getenv("BOT_TOKEN", ""))
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", os.getenv("CHAT_ID", ""))

# Псевдонимы для импорта в bot.py
BOT_TOKEN = TELEGRAM_BOT_TOKEN
CHAT_ID = TELEGRAM_CHAT_ID

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")

# Настройки базы данных и работы бота
DB_FILE = os.getenv("DB_FILE", "jobs.db")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", 60))
MAX_JOBS_PER_CHECK = int(os.getenv("MAX_JOBS_PER_CHECK", 10))

@dataclass
class TrackConfig:
    name: str
    search_keywords: List[str]
    keywords: List[str]
    negative_keywords: List[str] = field(default_factory=list)

TRACKS = [
    TrackConfig(
        name="DOCS & DOCS-AS-CODE (Mid/Senior)",
        search_keywords=[
            "technical writer", "documentation engineer", "docs as code", 
            "docs-as-code", "api documentation", "developer documentation", "docs"
        ],
        keywords=[
            "technical writer", "documentation engineer", "docs-as-code", 
            "api documentation", "developer documentation", "markdown", 
            "git", "openapi", "swagger", "sphinx", "mkdocs"
        ],
        negative_keywords=[
            "junior", "intern", "support", "customer support", "copywriter"
        ]
    ),
    TrackConfig(
        name="TECH & BACKEND (Junior)",
        search_keywords=["python", "backend", "qa", "api qa", "devops", "automation"],
        keywords=["python", "backend", "qa", "testing", "devops", "automation", "api"],
        negative_keywords=[
            "senior", "lead", "principal", "head", "architect", "support", 
            "customer support", "helpdesk"
        ]
    ),
    TrackConfig(
        name="WEATHER & CLIMATE TECH",
        search_keywords=["meteorology", "weather", "climate", "atmospheric"],
        keywords=["meteorology", "weather", "climate", "atmospheric", "data", "python", "gis"],
        negative_keywords=["sales", "account manager", "commercial"]
    )
]

TECH_STACK_KEYWORDS = ["python", "git", "markdown", "api", "rest", "swagger", "openapi", "docker", "ci/cd"]
import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", os.getenv("BOT_TOKEN", ""))
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", os.getenv("CHAT_ID", ""))

BOT_TOKEN = TELEGRAM_BOT_TOKEN
CHAT_ID = TELEGRAM_CHAT_ID

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")

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
        name="🕵️‍♂️ RESEARCH & TECHNICAL INVESTIGATION",
        search_keywords=[
            "technical writer", "documentation engineer", "research analyst", 
            "research engineer", "research technician", "scientific technician",
            "technical-scientific staff", "laboratory engineer", "api documentation"
        ],
        keywords=[
            "research", "investigate", "troubleshoot", "debug", "analyze", 
            "verify", "root cause", "trace", "api", "python",
            "documentation", "git", "knowledge base", "rag"
        ],
        negative_keywords=[
            "senior", "sr.", "staff", "lead", "principal", "head", "architect", 
            "vp", "sales", "account manager", "commercial", "customer support", "helpdesk"
        ]
    ),
    TrackConfig(
        name="🐍 PYTHON, BACKEND & AUTOMATION",
        search_keywords=[
            "python", "backend", "automation", "research software", 
            "data analyst", "scientific", "scripting", "measurement engineer"
        ],
        keywords=[
            "python", "backend", "api", "rest", "json", "git", "github", 
            "automation", "database", "postgresql", "sql", "docker", "troubleshoot"
        ],
        negative_keywords=[
            "senior", "sr.", "staff", "lead", "principal", "head", "architect", 
            "manager", "director", "support", "helpdesk", "customer support"
        ]
    ),
    TrackConfig(
        name="🌍 WEATHER, CLIMATE & SCIENTIFIC TECH",
        search_keywords=[
            "meteorology", "weather", "climate", "atmospheric", "remote sensing", 
            "satellite", "environmental", "geospatial", "science",
            "scientific instrumentation", "environmental monitoring", 
            "atmospheric instrumentation", "observational scientist", "field engineer"
        ],
        keywords=[
            "meteorology", "weather", "climate", "atmospheric", "science", 
            "python", "gis", "satellite", "data analysis", "remote sensing", 
            "environmental", "xarray", "numpy", "netcdf", "grib", "forecast"
        ],
        negative_keywords=[
            "sales", "account manager", "commercial", "manager", "lead"
        ]
    )
]

TECH_STACK_KEYWORDS = ["python", "git", "markdown", "api", "rest", "swagger", "openapi", "docker", "ci/cd", "postgresql", "xarray", "netcdf"]
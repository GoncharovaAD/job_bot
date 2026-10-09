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
MAX_JOBS_PER_CHECK = int(os.getenv("MAX_JOBS_PER_CHECK", 15))

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
            "technical research", "research engineer", "research analyst", 
            "research technician", "scientific technician", "technical-scientific staff", 
            "laboratory engineer", "api documentation"
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
        name="⚡ PYTHON, DATA, LINUX & HARDWARE / ROBOTICS",
        search_keywords=[
            "python developer", "embedded python", "robotics software engineer", 
            "instrumentation engineer", "firmware engineer", "iot engineer", 
            "esp32", "sensor data engineer", "hardware software"
        ],
        keywords=[
            "python", "data", "api", "git", "linux", "electronics", 
            "soldering", "esp32", "sensors", "instrumentation", "robotics", "embedded"
        ],
        negative_keywords=[
            "senior", "sr.", "staff", "lead", "principal", "head", "architect", 
            "manager", "director", "support", "customer support"
        ]
    ),
    TrackConfig(
        name="🌍 WEATHER, CLIMATE & SCIENTIFIC TECH",
        search_keywords=[
            "meteorology", "weather", "climate", "atmospheric", "remote sensing", 
            "satellite data", "environmental data", "geospatial data", "scientific data",
            "environmental monitoring", "observational scientist"
        ],
        keywords=[
            "meteorology", "weather", "climate", "atmospheric", "science", 
            "python", "gis", "satellite", "data analysis", "remote sensing", 
            "environmental", "sensors", "instrumentation"
        ],
        negative_keywords=[
            "sales", "account manager", "commercial", "manager", "lead"
        ]
    ),
    TrackConfig(
        name="✍️ JUNIOR TECHNICAL WRITER (Friend's Track)",
        search_keywords=[
            "junior technical writer", "technical writer", "documentation specialist", 
            "junior documentation engineer", "api documentation writer"
        ],
        keywords=[
            "technical writer", "documentation", "api documentation", "markdown", 
            "git", "writer", "manual", "guide", "confluence"
        ],
        negative_keywords=[
            "senior", "sr.", "lead", "principal", "head", "architect", 
            "manager", "director", "staff", "5+ years", "3+ years"
        ]
    )
]

TECH_STACK_KEYWORDS = ["python", "git", "linux", "markdown", "api", "rest", "esp32", "sensors", "docker", "postgresql", "xarray"]
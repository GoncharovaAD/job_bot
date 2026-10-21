import os
from dataclasses import dataclass
from typing import List

# Путь к файлу базы данных SQLite
DB_FILE = "jobs_database.db"

@dataclass
class TrackConfig:
    name: str
    search_keywords: List[str]
    keywords: List[str]
    negative_keywords: List[str]

# ---------------------------------------------------------------------------
# API KEY CONFIGURATION
# ---------------------------------------------------------------------------
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.environ.get("ADZUNA_APP_KEY", "")

# ---------------------------------------------------------------------------
# BOT TIMINGS & LIMITS
# ---------------------------------------------------------------------------
CHECK_INTERVAL_MINUTES = int(os.environ.get("CHECK_INTERVAL_MINUTES", "60"))
MAX_JOBS_PER_CHECK = int(os.environ.get("MAX_JOBS_PER_CHECK", "15"))

# ---------------------------------------------------------------------------
# GLOBAL EXCLUSIONS (iGaming, Crypto, Fast-Paced Startups, Sole Writer)
# ---------------------------------------------------------------------------
GLOBAL_NEGATIVE_KEYWORDS = [
    # Toxic niches
    "casino", "gambling", "igaming", "betting", "poker", "slots",
    "crypto", "web3", "blockchain", "defi", "nft", "token",
    # Fast-paced / Burnout triggers
    "fast-paced", "fast paced", "hustle", "wear many hats", "hypergrowth",
    # Sole writer / High-stress roles
    "sole technical writer", "first technical writer", "single technical writer",
    "solo writer", "sole writer"
]

# ---------------------------------------------------------------------------
# TRACK CONFIGURATIONS
# ---------------------------------------------------------------------------
TRACKS = [
    # -----------------------------------------------------------------------
    # 1. ANNA: SENIOR / LEAD DOCS ENGINEER (MedTech, Pharma & Regulated)
    # -----------------------------------------------------------------------
    TrackConfig(
        name="🏥 ANNA | MedTech, Pharma & Regulated Systems",
        search_keywords=[
            "medical device technical writer", "clinical documentation engineer",
            "regulatory technical writer", "healthcare technical writer",
            "validation technical writer", "biotech documentation",
            "pharma technical writer", "clinical data writer"
        ],
        keywords=[
            "medtech", "healthcare", "pharma", "biotech", "clinical", "regulatory",
            "validation", "gcp", "sop", "edc", "fda", "iso 13485", "healthtech",
            "documentation", "technical writer", "docs-as-code", "markdown",
            "confluence", "git", "python", "sql", "json", "postman"
        ],
        negative_keywords=GLOBAL_NEGATIVE_KEYWORDS + [
            "junior", "entry level", "intern", "8+ years", "10+ years"
        ]
    ),

    # -----------------------------------------------------------------------
    # 2. ANNA: CLEANTECH, ENVIRONMENTAL IOT & DATA ENGINEERING
    # -----------------------------------------------------------------------
    TrackConfig(
        name="🌿 ANNA | CleanTech, Environmental IoT & Meteorology",
        search_keywords=[
            "environmental data engineer", "iot documentation engineer",
            "weather data engineer", "cleantech technical writer",
            "gis documentation", "sensor data writer", "scientific data engineer"
        ],
        keywords=[
            "cleantech", "iot", "sensors", "esp32", "environmental", "weather",
            "meteorology", "gis", "remote sensing", "python", "postgresql",
            "sql", "github actions", "mkdocs", "markdown", "api", "xarray",
            "netcdf", "grib", "documentation", "docs-as-code"
        ],
        negative_keywords=GLOBAL_NEGATIVE_KEYWORDS + [
            "junior", "entry level", "intern"
        ]
    ),

    # -----------------------------------------------------------------------
    # 3. DIANA: STABLE & CALM TECHNICAL WRITING (Mid/Junior+, 0.5–3 yrs)
    # -----------------------------------------------------------------------
    TrackConfig(
        name="☕ DIANA | Calm & Stable Technical Writer",
        search_keywords=[
            "technical writer", "documentation writer", "software technical writer",
            "junior technical writer", "technical author", "api documentation writer",
            "technical documentation specialist"
        ],
        keywords=[
            "technical writer", "documentation", "markdown", "confluence",
            "git", "api", "rest", "json", "manual", "guide", "sop", "clinical",
            "healthcare", "saas", "user guide", "internal documentation"
        ],
        negative_keywords=GLOBAL_NEGATIVE_KEYWORDS + [
            "senior", "sr.", "lead", "principal", "head of", "director", "architect",
            "5+ years", "6+ years", "7+ years", "8+ years"
        ]
    )
]
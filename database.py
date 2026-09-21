import os
import psycopg2
from config import DB_FILE # На случай фолбэка

DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    def __init__(self):
        if DATABASE_URL:
            self.conn = psycopg2.connect(DATABASE_URL)
            self._init_db_postgres()
        else:
            # Резервный фолбэк на SQLite, если DATABASE_URL не задан
            import sqlite3
            self.conn = sqlite3.connect(DB_FILE)
            self._init_db_sqlite()

    def _init_db_postgres(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS seen_jobs (
                    dedup_hash TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()

    def _init_db_sqlite(self):
        with self.conn as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS seen_jobs (
                    dedup_hash TEXT PRIMARY KEY,
                    source_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

    def is_duplicate(self, dedup_hash: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("SELECT 1 FROM seen_jobs WHERE dedup_hash = %s", (dedup_hash,))
            return cur.fetchone() is not None

    def mark_seen(self, dedup_hash: str, source_id: str):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO seen_jobs (dedup_hash, source_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (dedup_hash, source_id)
            )
            self.conn.commit()
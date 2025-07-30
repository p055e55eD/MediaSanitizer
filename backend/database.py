# backend/database.py

import sqlite3
import json
import os
from datetime import datetime

# Always use a path relative to THIS file for SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), "../database/articles.db")

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.create_tables()

    def connect(self):
        """Creates a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        """Creates required tables if they do not exist."""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    url TEXT PRIMARY KEY,
                    title TEXT,
                    domain TEXT,
                    content TEXT,
                    report_json TEXT,
                    analyzed_at TEXT
                )
            """)
            conn.commit()

    def save_analysis(self, url, title, domain, content, analysis):
        report_json = json.dumps(analysis, ensure_ascii=False)
        analyzed_at = datetime.utcnow().isoformat()
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO articles (url, title, domain, content, report_json, analyzed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (url, title, domain, content, report_json, analyzed_at))
            conn.commit()

    def get_analysis(self, url):
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT report_json FROM articles WHERE url = ?", (url,))
            row = c.fetchone()
            if row:
                return json.loads(row[0])
            return None

    def count_articles(self):
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM articles")
            result = c.fetchone()
            return result[0] if result else 0

    def last_analyzed(self):
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT MAX(analyzed_at) FROM articles")
            result = c.fetchone()
            return result[0] if result else None

    def clear_articles(self):
        """Delete all articles from the database."""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM articles")
            conn.commit()

# --- Singleton for easy import in app.py ---
db = Database()

def init_db():
    """Standalone DB initialization (for setup scripts)"""
    Database().create_tables()
    print("Database and tables created (if not existed).")

# ---- Example usage for testing/initializing ----
if __name__ == "__main__":
    print("Running database.py directly.")
    init_db()
    print("Tested DB initialization.")

    # (Optional) Uncomment to clear DB:
    # db.clear_articles()
    # print("All articles cleared.")

    # Test insert
    fake_report = {
        "credibility_score": 90,
        "red_flags": [],
        "entities": [["Example Person", "PERSON"]],
        "summary": "This is a test summary.",
        "language": "en"
    }
    url = "https://civilnet.am/news/example-article"
    db.save_analysis(
        url=url,
        title="Example Article",
        domain="civilnet.am",
        content="Some example article text.",
        analysis=fake_report
    )
    print(db.get_analysis(url))
    print(f"Total articles: {db.count_articles()}")
    print(f"Last analyzed: {db.last_analyzed()}")

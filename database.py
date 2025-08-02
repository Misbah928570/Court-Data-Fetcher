import sqlite3
from datetime import datetime

DB_NAME = "court_queries.db"

# Run once at app start to create the table
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_number TEXT,
            filing_year TEXT,
            query_time TEXT,
            raw_response TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Called every time user submits a case
def log_query(case_type, case_number, filing_year, raw_response):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO query_logs (case_type, case_number, filing_year, query_time, raw_response)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        case_type,
        case_number,
        filing_year,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        raw_response
    ))
    conn.commit()
    conn.close()

import sqlite3
from pathlib import Path

DB_PATH = Path("data/planejador.db")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        age INTEGER,
        horizon_years INTEGER,
        situation TEXT,
        initial_patrimony REAL,
        monthly_contribution REAL,
        desired_monthly_income REAL,
        minimum_monthly_income REAL,
        risk_profile TEXT,
        liquidity_months REAL,
        other_monthly_income REAL,
        notes TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        name TEXT,
        asset_class TEXT NOT NULL,
        quantity REAL DEFAULT 0,
        unit_price REAL DEFAULT 0,
        total_value REAL DEFAULT 0,
        target_percent REAL DEFAULT 0,
        current_percent REAL DEFAULT 0,
        action TEXT DEFAULT 'MANTER',
        notes TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS macro_snapshot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reference_date TEXT NOT NULL,
        selic REAL,
        ipca_12m REAL,
        ipca_ytd REAL,
        inflation_expectation REAL,
        selic_expectation REAL,
        source TEXT,
        notes TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS allocation_targets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_class TEXT UNIQUE NOT NULL,
        target_percent REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

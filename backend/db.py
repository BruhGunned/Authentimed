import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from datetime import datetime

# Load .env from backend folder (so it works even when running from project root)
_backend_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_backend_dir, ".env"))

# --- Online (Supabase) connection: uncomment below and comment the line above to use .env ---
_raw_url = os.getenv("DATABASE_URL")
DATABASE_URL = _raw_url.strip() if (_raw_url and _raw_url.strip()) else "postgresql://localhost:5432/authentimed"
if "supabase.com" in DATABASE_URL and "sslmode" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL + ("&" if "?" in DATABASE_URL else "?") + "sslmode=require"


def get_connection():
    return psycopg2.connect(DATABASE_URL)



def _conn(url=None):
    """Connection using DATABASE_URL or optional url."""
    return psycopg2.connect(url or DATABASE_URL)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            product_id TEXT PRIMARY KEY,
            first_scan_time TIMESTAMP,
            scan_count INTEGER,
            last_scan_time TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS code_mappings (
            code TEXT PRIMARY KEY
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def code_exists(code, database_url=None):
    """Return True if PAN code already exists in code_mappings."""
    conn = _conn(database_url)
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM code_mappings WHERE code = %s", (code,))
        return cur.fetchone() is not None
    finally:
        cur.close()
        conn.close()


def insert_mapping(code, _value=None, database_url=None):
    """Insert a PAN code into code_mappings (value unused, for API compatibility)."""
    conn = _conn(database_url)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO code_mappings (code) VALUES (%s)", (code,))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def record_scan(product_id):
    conn = get_connection()
    cur = conn.cursor()

    now = datetime.utcnow()

    cur.execute("SELECT * FROM scans WHERE product_id = %s", (product_id,))
    row = cur.fetchone()

    if row:
        cur.execute("""
            UPDATE scans
            SET scan_count = scan_count + 1,
                last_scan_time = %s
            WHERE product_id = %s
        """, (now, product_id))
    else:
        cur.execute("""
            INSERT INTO scans (product_id, first_scan_time, scan_count, last_scan_time)
            VALUES (%s, %s, %s, %s)
        """, (product_id, now, 1, now))

    conn.commit()
    cur.close()
    conn.close()


def get_scan_info(product_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM scans WHERE product_id = %s", (product_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    return row

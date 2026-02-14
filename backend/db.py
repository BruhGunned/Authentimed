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

    # Product–code link for verification (Supabase / plan §3.1)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            pan_code TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'utc')
        )
    """)

    # Pharmacist: one scan per product (plan §3.2)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pharmacist_scans (
            product_id TEXT PRIMARY KEY,
            scanned_at TIMESTAMP NOT NULL
        )
    """)

    # Consumer: one scan per factor per product (plan §3.3)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS consumer_scans (
            product_id TEXT NOT NULL,
            factor TEXT NOT NULL CHECK (factor IN ('qr', 'strip')),
            scanned_at TIMESTAMP NOT NULL,
            PRIMARY KEY (product_id, factor)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def code_exists(code, database_url=None):
    """Return True if PAN code already exists in products (used by code_generator for uniqueness)."""
    if not code or not str(code).strip():
        return True
    conn = _conn(database_url)
    cur = conn.cursor()
    try:
        normalized = str(code).strip().upper()
        cur.execute("SELECT 1 FROM products WHERE UPPER(TRIM(pan_code)) = %s", (normalized,))
        return cur.fetchone() is not None
    finally:
        cur.close()
        conn.close()


def insert_mapping(code, _value=None, database_url=None):
    """No-op: codes are stored in products when insert_product is called. Kept for code_generator API."""
    pass


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


# ========== Products (product_id <-> pan_code) ==========

def insert_product(product_id, pan_code):
    """Store product_id and pan_code link for verification. pan_code is stored normalized (trim, upper)."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        pid = (product_id or "").strip()
        code = (pan_code or "").strip().upper()
        if not pid or not code:
            return
        cur.execute(
            "INSERT INTO products (product_id, pan_code) VALUES (%s, %s)",
            (pid, code)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def get_product_by_id(product_id):
    """Get product row by product_id. Returns dict or None. Only returns a row if product was issued by manufacturer (exists in products)."""
    pid = (product_id or "").strip()
    if not pid:
        return None
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM products WHERE product_id = %s", (pid,))
        row = cur.fetchone()
        if row and (row.get("product_id") or "").strip() != pid:
            return None
        return row
    except Exception:
        return None
    finally:
        cur.close()
        conn.close()


def get_product_by_pan_code(pan_code):
    """Get product row by pan_code (for strip verification). Returns dict or None. Match is case-insensitive and trim-safe."""
    if not pan_code or not str(pan_code).strip():
        return None
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        normalized = str(pan_code).strip().upper()
        cur.execute("SELECT * FROM products WHERE UPPER(TRIM(pan_code)) = %s", (normalized,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


# ========== Pharmacist scans (one per product) ==========

def get_pharmacist_scan(product_id):
    """Return scan row if pharmacist already scanned this product, else None."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM pharmacist_scans WHERE product_id = %s", (product_id,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def record_pharmacist_scan(product_id):
    """Record that a pharmacist scanned this product (one scan allowed per product)."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        now = datetime.utcnow()
        cur.execute(
            "INSERT INTO pharmacist_scans (product_id, scanned_at) VALUES (%s, %s)",
            (product_id, now)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


# ========== Consumer scans (one verification per product; flag if already scanned via any factor) ==========

def get_consumer_scan(product_id, factor):
    """Return scan row if consumer already scanned this product with this factor, else None."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            "SELECT * FROM consumer_scans WHERE product_id = %s AND factor = %s",
            (product_id, factor)
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def get_any_consumer_scan(product_id):
    """Return any existing consumer scan for this product (QR or strip). Used to allow only one verification per product."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM consumer_scans WHERE product_id = %s LIMIT 1", (product_id,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def record_consumer_scan(product_id, factor):
    """Record consumer scan for this product and factor (one scan per factor per product)."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        now = datetime.utcnow()
        cur.execute(
            "INSERT INTO consumer_scans (product_id, factor, scanned_at) VALUES (%s, %s, %s)",
            (product_id, factor, now)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

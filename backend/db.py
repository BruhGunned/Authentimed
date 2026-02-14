import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/authentimed")



def get_connection():
    return psycopg2.connect(DATABASE_URL)



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

    conn.commit()
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

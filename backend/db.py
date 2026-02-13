import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Default temporary PostgreSQL URL (override with DATABASE_URL for production/original db)
_DEFAULT_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://localhost:5432/authentimed_temp",
)

# Global connection cache per URL (singleton per URL)
_connections = {}


def get_db_connection(database_url=None):
    """
    Get a database connection to PostgreSQL.

    Uses a temporary DB by default; set DATABASE_URL to point to the original db later.

    Args:
        database_url: PostgreSQL connection URL (optional).
                      If None, uses DATABASE_URL env var or default local temp db.

    Returns:
        psycopg2 connection with RealDictCursor
    """
    global _connections
    url = database_url or _DEFAULT_DATABASE_URL
    if url not in _connections:
        conn = psycopg2.connect(url, cursor_factory=RealDictCursor)
        conn.autocommit = False
        _connections[url] = conn
    return _connections[url]


def init_db(database_url=None):
    """
    Initialize the database and create necessary tables.

    Args:
        database_url: PostgreSQL connection URL (optional). Uses default if None.
    """
    conn = get_db_connection(database_url)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS codes (
                id SERIAL PRIMARY KEY,
                code TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_code ON codes(code)
        """)
    conn.commit()


def code_exists(code, database_url=None):
    """
    Check if a code already exists in the database.

    Args:
        code: The code to check
        database_url: PostgreSQL connection URL (optional). Uses default if None.

    Returns:
        True if code exists, False otherwise
    """
    conn = get_db_connection(database_url)
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM codes WHERE code = %s LIMIT 1", (code,))
        result = cur.fetchone()
    return result is not None


def insert_mapping(code, value, database_url=None):
    """
    Insert a code mapping into the database (upsert: replace if code exists).

    Args:
        code: The code to insert
        value: The value to associate with the code
        database_url: PostgreSQL connection URL (optional). Uses default if None.

    Returns:
        The row ID of the inserted or updated record
    """
    conn = get_db_connection(database_url)
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO codes (code, value) VALUES (%s, %s)
            ON CONFLICT (code) DO UPDATE SET value = EXCLUDED.value
            RETURNING id
            """,
            (code, value),
        )
        row = cur.fetchone()
        row_id = row["id"] if row else None
    conn.commit()
    return row_id

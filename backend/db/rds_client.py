import psycopg2
from psycopg2.extras import RealDictCursor
from core import settings


def get_rds_connection():
    conn = psycopg2.connect(
        host=settings.RDS_HOST,
        port=settings.RDS_PORT,
        database=settings.RDS_DB,
        user=settings.RDS_USER,
        password=settings.RDS_PASSWORD,
        cursor_factory=RealDictCursor,
    )
    return conn


def fetch_all(query: str, params=None):
    conn = get_rds_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
        return rows
    finally:
        conn.close()


def fetch_one(query: str, params=None):
    conn = get_rds_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            row = cur.fetchone()
        return row
    finally:
        conn.close()

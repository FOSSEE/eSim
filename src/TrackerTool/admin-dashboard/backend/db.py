import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date, timedelta

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5435")),
        dbname=os.getenv("DB_NAME", "esim_tracker"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        sslmode=os.getenv("DB_SSLMODE", "prefer"),
    )

def execute_returning_one(sql: str, params=None):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params or [])
            row = cur.fetchone()
            conn.commit()
            return _row_to_dict(row) if row else None
    finally:
        conn.close()

        
from datetime import datetime, date, timedelta

def _json_safe(v):
    if isinstance(v, datetime):
        return v.isoformat(" ")
    elif isinstance(v, date):
        return v.isoformat()
    elif isinstance(v, timedelta):
        return round(v.total_seconds() / 3600, 6)
    return v

def _row_to_dict(row):
    d = dict(row)
    return {k: _json_safe(v) for k, v in d.items()}

def fetch_all(sql: str, params=None):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params or [])
            rows = cur.fetchall()
            return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()

def fetch_one(sql: str, params=None):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params or [])
            row = cur.fetchone()

            sql_start = sql.lstrip().split(None, 1)[0].upper() if sql.strip() else ""
            if sql_start in {"INSERT", "UPDATE", "DELETE"}:
                conn.commit()

            return _row_to_dict(row) if row else None
    finally:
        conn.close()

def execute(sql: str, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or [])
            conn.commit()
            return cur.rowcount
    finally:
        conn.close()
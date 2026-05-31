import sqlite3
import uuid
import hashlib
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "proxy.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id          TEXT PRIMARY KEY,
                email       TEXT UNIQUE NOT NULL,
                password    TEXT NOT NULL,
                api_key     TEXT UNIQUE NOT NULL,
                active      INTEGER DEFAULT 1,
                created_at  TEXT NOT NULL
            )
        """)
        conn.commit()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def generate_api_key() -> str:
    return "sk-" + uuid.uuid4().hex + uuid.uuid4().hex


# ── Customer ops ──────────────────────────────────────────────────────────────

def create_customer(email: str, password: str) -> dict:
    customer_id = str(uuid.uuid4())
    api_key = generate_api_key()
    now = datetime.utcnow().isoformat()

    with get_conn() as conn:
        try:
            conn.execute(
                "INSERT INTO customers (id, email, password, api_key, active, created_at) VALUES (?, ?, ?, ?, 1, ?)",
                (customer_id, email.lower(), hash_password(password), api_key, now),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Email already registered")

    return {"id": customer_id, "email": email, "api_key": api_key}


def get_customer_by_email(email: str, password: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM customers WHERE email = ? AND password = ? AND active = 1",
            (email.lower(), hash_password(password)),
        ).fetchone()
    return dict(row) if row else None


def get_customer_by_api_key(api_key: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM customers WHERE api_key = ? AND active = 1",
            (api_key,),
        ).fetchone()
    return dict(row) if row else None
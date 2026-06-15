import os
import sqlite3

DATABASE_URL = os.environ.get("DATABASE_URL", "").replace("postgres://", "postgresql://", 1)
USE_POSTGRES = bool(DATABASE_URL)

if USE_POSTGRES:
    import psycopg2

DB_PATH = "database/blogs.db"

def get_conn():
    return psycopg2.connect(DATABASE_URL) if USE_POSTGRES else sqlite3.connect(DB_PATH)

def ph():
    """Return the right placeholder for the current DB."""
    return "%s" if USE_POSTGRES else "?"

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    id_col = "SERIAL PRIMARY KEY" if USE_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS blogs(
            id {id_col},
            title TEXT, topic TEXT, content TEXT, image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Add image column if missing (SQLite only — Postgres handled by CREATE TABLE)
    if not USE_POSTGRES:
        try:
            cur.execute("ALTER TABLE blogs ADD COLUMN image TEXT")
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()


def save_blog(title, topic, content, image=""):
    conn = get_conn()
    cur = conn.cursor()
    p = ph()
    cur.execute(f"SELECT id FROM blogs WHERE title = {p}", (title,))
    if cur.fetchone():
        conn.close()
        print(f"Already exists: {title}")
        return False
    cur.execute(
        f"INSERT INTO blogs(title, topic, content, image) VALUES({p},{p},{p},{p})",
        (title, topic, content, image)
    )
    conn.commit()
    conn.close()
    print(f"Saved: {title}")
    return True


def get_all_blogs():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blogs ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_blog(blog_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM blogs WHERE id = {ph()}", (blog_id,))
    row = cur.fetchone()
    conn.close()
    return row
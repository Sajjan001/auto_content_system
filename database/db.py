import os
import sqlite3

# Check if DATABASE_URL is set (PostgreSQL on Render)
DATABASE_URL = os.environ.get("DATABASE_URL")

# Render sets DATABASE_URL starting with "postgres://" but psycopg2 needs "postgresql://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

USE_POSTGRES = bool(DATABASE_URL)

if USE_POSTGRES:
    import psycopg2
    import psycopg2.extras
    print("[DB] Using PostgreSQL (Render)")
else:
    print("[DB] Using SQLite (local development)")
    DB_PATH = "database/blogs.db"


def get_conn():
    if USE_POSTGRES:
        return psycopg2.connect(DATABASE_URL)
    else:
        return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    if USE_POSTGRES:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS blogs(
            id SERIAL PRIMARY KEY,
            title TEXT,
            topic TEXT,
            content TEXT,
            image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        # Add image column if not exists (migration safety)
        cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name='blogs' AND column_name='image'
            ) THEN
                ALTER TABLE blogs ADD COLUMN image TEXT;
            END IF;
        END $$;
        """)
    else:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS blogs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            topic TEXT,
            content TEXT,
            image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        try:
            cursor.execute("ALTER TABLE blogs ADD COLUMN image TEXT")
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully")


def save_blog(title, topic, content, image=""):
    try:
        conn = get_conn()
        cursor = conn.cursor()

        if USE_POSTGRES:
            cursor.execute("SELECT id FROM blogs WHERE title = %s", (title,))
        else:
            cursor.execute("SELECT id FROM blogs WHERE title = ?", (title,))

        if cursor.fetchone():
            conn.close()
            print(f"[DB] Duplicate blocked (title already exists): {title}")
            return False

        if USE_POSTGRES:
            cursor.execute("""
            INSERT INTO blogs(title, topic, content, image)
            VALUES(%s, %s, %s, %s)
            """, (title, topic, content, image))
        else:
            cursor.execute("""
            INSERT INTO blogs(title, topic, content, image)
            VALUES(?,?,?,?)
            """, (title, topic, content, image))

        conn.commit()
        conn.close()
        print(f"[DB] Blog saved successfully: {title}")
        return True
    except Exception as e:
        print(f"[DB] ERROR in save_blog: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_all_blogs():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM blogs
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_blog(blog_id):
    conn = get_conn()
    cursor = conn.cursor()

    if USE_POSTGRES:
        cursor.execute("""
        SELECT * FROM blogs
        WHERE id=%s
        """, (blog_id,))
    else:
        cursor.execute("""
        SELECT * FROM blogs
        WHERE id=?
        """, (blog_id,))

    row = cursor.fetchone()
    conn.close()
    return row
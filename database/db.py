import sqlite3

DB_PATH = "database/blogs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

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


def save_blog(title, topic, content, image=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM blogs WHERE title = ?", (title,))
    if cursor.fetchone():
        conn.close()
        print(f"Duplicate blocked: {title}")
        return False

    cursor.execute("""
    INSERT INTO blogs(title, topic, content, image)
    VALUES(?,?,?,?)
    """, (title, topic, content, image))

    conn.commit()
    conn.close()
    print(f"Blog saved: {title}")
    return True


def get_all_blogs():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM blogs
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_blog(blog_id):
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM blogs
    WHERE id=?
    """, (blog_id,))

    row = cursor.fetchone()

    conn.close()

    return row
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "post_history.db")


def init_db():
    """📂 Создаёт таблицу для хранения истории постов, если её нет"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS post_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_text TEXT UNIQUE
            )"""
        )
        conn.commit()


def is_duplicate_post(new_post):
    """🔄 Проверяет, был ли уже опубликован этот пост"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM post_history WHERE post_text = ?", (new_post,))
        return cursor.fetchone() is not None


def add_post_to_history(new_post):
    """✅ Добавляет пост в историю"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO post_history (post_text) VALUES (?)", (new_post,))
        conn.commit()


def clear_old_posts(limit=100):
    """🗑 Оставляет только последние 100 постов, удаляя старые"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM post_history WHERE id NOT IN (SELECT id FROM post_history ORDER BY id DESC LIMIT ?)",
            (limit,),
        )
        conn.commit()


# Инициализируем базу данных при запуске
init_db()

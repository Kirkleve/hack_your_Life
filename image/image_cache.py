"""
Файл отвечает за кэширование изображений, чтобы избежать повторов при публикации.

🔹 Создание базы кэша: Хранит URL изображений и их хэши.
🔹 Проверка дубликатов: Определяет, использовалось ли изображение ранее.
🔹 Сохранение изображений: Записывает новые изображения в базу.
🔹 Очистка кэша: Позволяет удалить все сохранённые изображения.
"""

import sqlite3
import os

# Путь к базе данных
DB_PATH = os.path.join(os.path.dirname(__file__), "image_cache.db")


def init_db():
    """📂 Создаёт таблицу для хранения кэша изображений"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS image_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_url TEXT UNIQUE,
                image_hash TEXT
            )"""
        )
        conn.commit()


def is_duplicate(image_url):
    """🔍 Проверяет, использовалось ли изображение ранее"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM image_cache WHERE image_url = ?", (image_url,))
        return cursor.fetchone() is not None


def cache_image(image_url, image_hash):
    """💾 Добавляет изображение в кэш"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO image_cache (image_url, image_hash) VALUES (?, ?)",
            (image_url, image_hash),
        )
        conn.commit()


def clear_cache():
    """❌ Удаляет все данные из кэша"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM image_cache")
        conn.commit()
        print("🗑 Кэш изображений очищен!")


# Инициализация базы данных при запуске
init_db()

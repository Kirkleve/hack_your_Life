"""
Файл отвечает за управление базой данных челленджей.

🔹 Инициализация базы: Создаёт таблицы `challenges` и `challenge_days`, если они отсутствуют.
🔹 Получение активного челленджа: Проверяет, есть ли уже запущенный челлендж.
🔹 Создание нового челленджа: Добавляет новый челлендж в базу и активирует его.
🔹 Деактивация старых челленджей: Автоматически отключает предыдущий челлендж перед запуском нового.
🔹 Запись дней челленджа: Сохраняет задания для каждого дня.
🔹 Логирование: Записывает все ключевые события (создание, добавление дней, активация).
"""

import os
import sqlite3
from datetime import datetime, timedelta

from logger import log_info

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "challenges.db")


def init_db():
    """Создаёт таблицы в базе данных, если их нет"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        announcement TEXT,
        start_date TEXT,
        end_date TEXT,
        last_used INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 0,
        pinned_message_id INTEGER DEFAULT NULL  -- ✅ Добавили поле для хранения ID закрепленного сообщения
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS challenge_days (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        challenge_id INTEGER,
        day_number INTEGER,
        text TEXT,
        FOREIGN KEY (challenge_id) REFERENCES challenges(id)
    )
    """)

    conn.commit()
    conn.close()
    log_info("✅ База данных проверена и обновлена!")


def get_active_challenge():
    """Получает текущий активный челлендж."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM challenges WHERE is_active = 1")
    challenge = cursor.fetchone()
    conn.close()
    return challenge


def start_new_challenge(name, description, announcement, days):
    """Добавляет новый челлендж и делает его активным."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    end_date = (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d")

    log_info(f"📌 Создаём новый челлендж: {name}")

    cursor.execute("UPDATE challenges SET is_active = 0 WHERE is_active = 1")  # Деактивируем старый челлендж
    cursor.execute("INSERT INTO challenges (name, description, announcement, start_date, end_date, is_active) VALUES (?, ?, ?, ?, ?, 1)",
                   (name, description, announcement, datetime.now().strftime("%Y-%m-%d"), end_date))

    challenge_id = cursor.lastrowid  # ID нового челленджа

    for day_number, text in enumerate(days, 1):
        log_info(f"✅ Добавляем день {day_number}: {text[:50]}...")
        cursor.execute("INSERT INTO challenge_days (challenge_id, day_number, text) VALUES (?, ?, ?)",
                       (challenge_id, day_number, text))

    conn.commit()
    conn.close()

    log_info(f"🎉 Челлендж успешно создан! ID: {challenge_id}")
    return challenge_id

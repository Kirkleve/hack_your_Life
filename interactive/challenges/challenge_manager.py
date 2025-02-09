"""
Файл отвечает за управление активными челленджами и их запуск.

🔹 Проверка текущего челленджа: Определяет, есть ли уже активный челлендж.
🔹 Выбор случайного челленджа: Берёт челлендж, который ещё не использовался.
🔹 Запуск нового челленджа: Активирует челлендж и отмечает его как использованный.
🔹 Отправка анонса: Публикует сообщение в Telegram о старте нового челленджа.
🔹 Обновление базы: Сбрасывает список, если все челленджи были использованы.
🔹 Логирование: Записывает все ключевые действия по управлению челленджами.
"""


import sqlite3
import asyncio
from interactive.challenges.challenge_db import get_active_challenge, start_new_challenge, DB_PATH
from telegram import Bot
from keys import TELEGRAM_BOT_TOKEN, CHAT_ID
from logger import log_info, log_error

bot = Bot(token=TELEGRAM_BOT_TOKEN)


def get_random_challenge():
    """Выбирает случайный челлендж, который ещё не использовался"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM challenges WHERE last_used = 0")
    remaining = cursor.fetchone()[0]

    if remaining == 0:
        log_info("🔄 Все челленджи были использованы! Сбрасываем список...")
        cursor.execute("UPDATE challenges SET last_used = 0")
        conn.commit()

    cursor.execute(
        "SELECT id, name, description, announcement FROM challenges WHERE last_used = 0 ORDER BY RANDOM() LIMIT 1")
    challenge = cursor.fetchone()

    if challenge:
        # Загружаем задания (days) для этого челленджа
        cursor.execute("SELECT day_number, text FROM challenge_days WHERE challenge_id = ? ORDER BY day_number",
                       (challenge[0],))
        days = [row[1] for row in cursor.fetchall()]
    else:
        days = []

    conn.close()
    return challenge, days  # Возвращаем также список заданий


async def send_challenge_announcement(name, announcement):
    """📢 Отправляет сообщение о старте нового челленджа"""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=announcement, parse_mode="Markdown")
        log_info("📢 Сообщение о старте челленджа отправлено в Telegram!")
    except Exception as e:
        log_error(f"❌ Ошибка при отправке сообщения о старте челленджа: {e}")


def mark_challenge_as_used(challenge_id):
    """Помечает челлендж как использованный"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE challenges SET last_used = 1 WHERE id = ?", (challenge_id,))
    conn.commit()
    conn.close()
    log_info(f"✅ Челлендж (ID: {challenge_id}) помечен как использованный!")


def check_and_start_new_challenge():
    """Запускает новый челлендж в понедельник и публикует сообщение о старте."""
    log_info("🔍 Проверяем активный челлендж...")
    active_challenge = get_active_challenge()

    if active_challenge:
        log_info(f"✅ Челлендж уже активен: {active_challenge[1]}")
        return

    log_info("⚠ Активного челленджа нет! Запускаем новый...")

    challenge, days = get_random_challenge()
    if not challenge:
        log_error("❌ В базе нет челленджей! Добавьте хотя бы один челлендж в `challenges.db`.")
        return

    if not days:
        log_error(f"❌ У челленджа '{challenge[1]}' нет заданий! Проверьте `challenge_days`.")
        return

    challenge_id = start_new_challenge(challenge[1], challenge[2], challenge[3], days)
    log_info(f"🎯 Новый челлендж запущен: {challenge[1]} (ID: {challenge_id})")

    mark_challenge_as_used(challenge[0])

    asyncio.create_task(send_challenge_announcement(challenge[1], challenge[3]))

"""
Файл отвечает за публикацию заданий челленджа в Telegram-канале.

🔹 Получение активного челленджа: Определяет, какой челлендж сейчас выполняется.
🔹 Вычисление текущего дня: Определяет, какое задание должно быть отправлено.
🔹 Открепление предыдущего сообщения: Снимает закреп с прошлого задания перед публикацией нового.
🔹 Отправка задания: Отправляет сообщение с заданием на текущий день.
🔹 Закрепление сообщения: Новое задание становится закреплённым в чате.
🔹 Удаление закрепа после завершения челленджа: Когда челлендж заканчивается, закреп снимается.
🔹 Логирование: Записывает успешные публикации и возможные ошибки.
"""

import sqlite3
from telegram import Bot
from keys import TELEGRAM_BOT_TOKEN, CHAT_ID
from interactive.challenges.challenge_db import get_active_challenge, DB_PATH
from logger import log_info, log_error

bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def unpin_old_challenge():
    """🔹 Асинхронно снимает старое закреплённое сообщение"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT pinned_message_id FROM challenges WHERE is_active = 1")
    pinned_message = cursor.fetchone()

    conn.close()

    if pinned_message and pinned_message[0]:
        try:
            await bot.unpin_chat_message(chat_id=CHAT_ID, message_id=pinned_message[0])
            log_info("📌 Старое сообщение с челленджем откреплено.")
        except Exception as e:
            log_error(f"⚠ Ошибка при откреплении старого сообщения: {e}")


async def post_challenge():
    """📢 Публикует задание текущего дня челленджа в Telegram-канале"""
    challenge = get_active_challenge()

    if not challenge:
        log_error("⚠ Ошибка: Активный челлендж не найден!")
        return

    log_info(f"✅ Найден активный челлендж: {challenge[1]} (ID: {challenge[0]})")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM challenge_days WHERE challenge_id = ?", (challenge[0],))
    total_days = cursor.fetchone()[0]

    cursor.execute("SELECT start_date FROM challenges WHERE id = ?", (challenge[0],))
    start_date = cursor.fetchone()[0]

    from datetime import datetime, timedelta
    today = datetime.now().date()
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    day_number = (today - start_date).days + 1

    if day_number > total_days:
        log_info("🏁 Челлендж завершён! Убираем закреп.")
        await unpin_old_challenge()  # ✅ Теперь вызываем с `await`
        return

    cursor.execute("SELECT text FROM challenge_days WHERE challenge_id = ? AND day_number = ?",
                   (challenge[0], day_number))
    task = cursor.fetchone()

    conn.close()

    if not task:
        log_error("⚠ Ошибка: Задание на текущий день не найдено!")
        return

    log_info(f"📢 Отправка челленджа: {challenge[1]} (День {day_number})")

    try:
        await unpin_old_challenge()  # ✅ Теперь корректный `await`
        msg = await bot.send_message(chat_id=CHAT_ID, text=f"🔥 {challenge[1]}\n\n{task[0]}")
        await bot.pin_chat_message(chat_id=CHAT_ID, message_id=msg.message_id)

        log_info(f"📌 Челлендж отправлен и закреплён: {msg.message_id}")

        # ✅ Записываем ID закрепленного сообщения в базу
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE challenges SET pinned_message_id = ? WHERE id = ?", (msg.message_id, challenge[0]))
        conn.commit()
        conn.close()

    except Exception as e:
        log_error(f"❌ Ошибка при отправке челленджа: {e}")

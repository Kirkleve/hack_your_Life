import random
from telegram import Bot
from keys import TELEGRAM_BOT_TOKEN, CHAT_ID
import asyncio
from logger import log_error

bot = Bot(token=TELEGRAM_BOT_TOKEN)

active_challenge = None

async def send_challenge_day():
    """🔥 Отправка челленджа дня + напоминание, если он не выполнен"""
    global active_challenge
    challenges = [
        "💪 День 1: 50 приседаний",
        "🏃 День 2: 10 минут бега",
        "📖 День 3: Прочитать 5 страниц книги",
        "💧 День 4: Выпить 2 литра воды",
        "🧘 День 5: 5 минут медитации"
    ]

    if active_challenge:
        try:
            await bot.send_message(chat_id=CHAT_ID, text=f"⏳ Не забывай про текущий челлендж: {active_challenge}")
        except Exception as e:
            log_error(f"❌ Ошибка при отправке напоминания о челлендже: {e}")
        return

    active_challenge = random.choice(challenges)

    try:
        await bot.send_message(chat_id=CHAT_ID, text=f"🔥 Челлендж дня: {active_challenge}")
        await asyncio.sleep(5)
    except Exception as e:
        log_error(f"❌ Ошибка при отправке челленджа: {e}")

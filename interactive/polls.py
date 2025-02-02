from telegram import Bot
from keys import TELEGRAM_BOT_TOKEN, CHAT_ID
from analytics import get_most_popular_topic
import asyncio
from logger import log_error

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_poll():
    """📊 Отправка обычного опроса в канал"""
    topic = get_most_popular_topic()
    question = "Какую тему ты хочешь видеть чаще?"
    options = ["Спорт", "Продуктивность", "Биохакинг", "Здоровье"]

    if "спорт" in topic.lower():
        question = "Какой вид спорта тебе интересен больше всего?"
        options = ["Бег", "Фитнес", "Плавание", "Йога"]

    try:
        await bot.send_poll(chat_id=CHAT_ID, question=question, options=options)
        await asyncio.sleep(5)
    except Exception as e:
        log_error(f"❌ Ошибка при отправке опроса: {e}")

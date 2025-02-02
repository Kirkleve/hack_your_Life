from telegram import Bot
from keys import TELEGRAM_BOT_TOKEN, CHAT_ID
from analytics import load_reaction_data
import asyncio
from logger import log_error


bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_weekly_summary():
    """📅 Подведение итогов недели с анализом активности подписчиков"""
    reaction_data = load_reaction_data()
    most_liked_topic = max(reaction_data, key=lambda topic: reaction_data[topic]["total_likes"], default="Нет данных")

    summary_text = (
        "📝 Итоги недели:\n"
        f"✔ Самая популярная тема: {most_liked_topic}\n"
        f"🔥 Количество реакций: {sum(topic['total_likes'] for topic in reaction_data.values())}\n"
        f"🏆 Лучший подписчик: @username (по лайкам)"
    )

    try:
        await bot.send_message(chat_id=CHAT_ID, text=summary_text)
        await asyncio.sleep(5)
    except Exception as e:
        log_error(f"❌ Ошибка при отправке недельного отчёта: {e}")

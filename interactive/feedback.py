"""
Файл отвечает за сбор обратной связи от подписчиков.

🔹 Определение популярной темы: Анализирует, какие посты вызвали наибольший интерес.
🔹 Генерация запроса: Формирует вопрос на основе популярной темы.
🔹 Отправка сообщения: Публикует запрос обратной связи в Telegram-канале.
🔹 Обработка ошибок: Логирует сбои при отправке сообщений.
"""

from telegram import Bot
from keys import TELEGRAM_BOT_TOKEN, CHAT_ID
from analytics import get_most_popular_topic
from logger import log_error

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_feedback_request():
    """💬 Запрос обратной связи на основе активности подписчиков"""
    topic = get_most_popular_topic()
    feedback_text = f"💬 Что вам больше всего понравилось в постах про {topic}? Напишите нам!"

    try:
        await bot.send_message(chat_id=CHAT_ID, text=feedback_text)
    except Exception as e:
        log_error(f"❌ Ошибка при запросе обратной связи: {e}")

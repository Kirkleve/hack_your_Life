"""
Файл отвечает за анализ популярных тем в Telegram-каналах.

🔹 Подключение к Telegram API: Использует Telethon и сохранённую сессию.
🔹 Мониторинг трендов: Анализирует посты из списка каналов (`TREND_CHANNELS`).
🔹 Фильтрация тем: Оставляет только темы, связанные с продуктивностью, спортом, здоровьем и мотивацией.
🔹 Оценка популярности: Учитывает количество реакций на сообщения.
🔹 Автоматический отбор: Возвращает 10 самых популярных тем для дальнейшего использования.
"""

from telethon import TelegramClient
from logger import log_error, log_info
from keys import API_ID, API_HASH  # 🔑 Импортируем API
from content_improvements.trend_channels import TREND_CHANNELS  # 🔍 Импортируем список каналов


SESSION_FILE = "trend_analyzer_session"  # ✅ Файл сессии Telegram

# ✅ Создаём клиент Telegram, который будет использовать сохранённую сессию
client = TelegramClient(SESSION_FILE, API_ID, API_HASH)

ALLOWED_KEYWORDS = ["здоровье", "спорт", "продуктивность", "мотивация", "биохакинг", "энергия", "сон", "цели"]


async def get_trending_topics():
    """📊 Получает популярные темы из Telegram-каналов (и использует сохранённую сессию)"""
    trending_topics = []

    try:
        async with client:
            log_info("✅ Подключено к Telegram API через сохранённую сессию!")

            for channel in TREND_CHANNELS:
                try:
                    async for message in client.iter_messages(channel, limit=30):
                        if message.message:
                            text = message.message.lower()
                            reactions = message.reactions
                            if reactions and any(kw in text for kw in ALLOWED_KEYWORDS):
                                topic = text[:50]  # Обрезаем до 50 символов для краткости
                                trending_topics.append((topic, sum(reaction.count for reaction in reactions.reactions)))

                except Exception as e:
                    log_error(f"Ошибка при получении трендов с {channel}: {e}")

        # Сортируем по популярности
        trending_topics.sort(key=lambda x: x[1], reverse=True)
        return [t[0] for t in trending_topics[:10]]

    except Exception as e:
        log_error(f"❌ Ошибка подключения к Telegram API: {e}")
        return []  # Возвращаем пустой список, чтобы избежать ошибок

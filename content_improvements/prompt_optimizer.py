import random
from content_improvements.trend_analyzer import get_trending_topics
from content_improvements.topics import topics  # 📌 Импорт списка тем
from logger import log_info


async def optimize_prompt(base_prompt, topic):
    """✍️ Оптимизирует промт для OpenAI, добавляя трендовую или стандартную тему."""
    try:
        # trending_topics = await get_trending_topics()  # ✅ Теперь `await` корректно работает
        trending_topics = random.choice(topics)
        if trending_topics:
            most_popular_trend = trending_topics[0]  # Берём самый популярный тренд
        else:
            most_popular_trend = random.choice(topics)  # 📌 Используем тему из topics.py
            log_info(f"⚠️ Нет трендов, выбрана случайная тема: {most_popular_trend}")

    except Exception as e:
        log_info(f"❌ Ошибка получения трендов: {e}")
        most_popular_trend = random.choice(topics)  # 📌 Если ошибка, используем тему из topics.py

    topic += f" ({most_popular_trend})"
    log_info(f"✅ Добавлен тренд: {most_popular_trend}")

    return base_prompt.replace("{topic}", topic)

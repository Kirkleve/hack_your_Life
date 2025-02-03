import requests
from bs4 import BeautifulSoup

# Ключевые слова, по которым определяем нужные нам тренды
ALLOWED_KEYWORDS = ["здоровье", "спорт", "продуктивность", "мотивация", "биохакинг", "энергия", "сон", "цели"]


def get_trending_topics():
    """📊 Парсер популярных тем из Telegram-каналов (оставляет только темы по нашей тематике)."""
    url = "https://tlgrm.ru/channels/popular"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    topics = [item.text for item in soup.select(".channel-item-title")]

    # ❌ Отбрасываем нерелевантные темы
    filtered_topics = [topic for topic in topics if any(keyword in topic.lower() for keyword in ALLOWED_KEYWORDS)]

    return filtered_topics[:10]  # Берём только 10 самых релевантных тем

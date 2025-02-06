import random
from content_improvements.topics import topics  # 📌 Импорт списка тем

used_topics = []  # 📌 Храним использованные темы, чтобы избежать повторов

def get_next_topic():
    """📌 Выбирает следующую тему, исключая уже использованные."""
    global used_topics

    if len(used_topics) == len(topics):
        used_topics = []  # Если все темы использованы, очищаем список

    available_topics = [topic for topic in topics if topic not in used_topics]
    next_topic = random.choice(available_topics)
    used_topics.append(next_topic)
    return next_topic

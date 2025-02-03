import random
from content_improvements.trend_analyzer import get_trending_topics


def optimize_prompt(base_prompt, topic):
    """✍️ Оптимизирует промт для OpenAI, добавляя трендовые темы."""
    trending_topics = get_trending_topics()

    if trending_topics:
        topic += f" ({random.choice(trending_topics)})"

    return base_prompt.replace("{topic}", topic)
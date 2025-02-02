import random
import openai
from keys import OPENAI_API_KEY
from topics import topics  # Импорт списка тем

# ✅ Устанавливаем API-ключ для OpenAI
openai.api_key = OPENAI_API_KEY

# ✅ Храним использованные темы, чтобы не повторялись подряд
used_topics = []

def get_next_topic():
    """📌 Выбор следующей темы, исключая уже использованные."""
    global used_topics
    if len(used_topics) == len(topics):
        used_topics = []  # Если все темы использованы, очищаем список

    available_topics = [topic for topic in topics if topic not in used_topics]
    next_topic = random.choice(available_topics)
    used_topics.append(next_topic)
    return next_topic


def generate_post(topic=None):
    """✍️ Генерация текста поста через OpenAI GPT-4."""

    if topic is None:
        topic = get_next_topic()

    prompt = (
        f"Напиши вдохновляющий, увлекательный и легко читаемый пост на тему: \"{topic}\". "
        "Текст должен быть грамотным и логичным, без ошибок, содержательным и полезным. "
        "Добавь интересные факты, конкретные примеры, полезные выводы и неожиданные открытия. "
        "Структурируй текст с абзацами и списками, чтобы он был лёгким для чтения. "
        "Используй дружелюбный, но серьёзный тон. "
        "Добавь немного эмодзи, чтобы текст выглядел живым, только если они подчёркивают смысл текста."
        "Структурируй материал в виде списков, но не перегружай визуальными элементами. "
        "Ограничение: не больше 2000 символов."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            timeout=30  # ✅ Ограничиваем время ожидания OpenAI API
        )
        return response["choices"][0]["message"]["content"].strip()

    except openai.error.Timeout:
        print("⏳ OpenAI API слишком долго отвечает. Пропускаем этот запрос.")
        return "Ошибка генерации поста. Попробуйте позже."

    except Exception as e:
        print(f"❌ Ошибка при генерации текста через OpenAI: {e}")
        return "Ошибка генерации поста."


def split_text_by_paragraphs(text, max_length=1024):
    """✂️ Разделение текста на заголовок и основную часть с учётом ограничения длины."""
    paragraphs = text.split('\n')  # Разделяем текст по абзацам
    if not paragraphs:
        return "", [""]  # Если нет текста, возвращаем пустые значения

    title = paragraphs[0]  # 🏆 Первый абзац — заголовок
    body = "\n".join(paragraphs[1:]).strip()  # Остальной текст

    # 🔹 Разбиваем основную часть на блоки (по 1024 символа)
    messages = []
    current_message = ""

    for paragraph in body.split('\n'):
        if len(current_message) + len(paragraph) + 1 <= max_length:
            current_message += (paragraph + "\n")
        else:
            messages.append(current_message.strip())
            current_message = paragraph + "\n"

    # Добавляем последний кусок текста
    if current_message.strip():
        messages.append(current_message.strip())

    return title, messages  # ✅ Заголовок + список частей основного текста

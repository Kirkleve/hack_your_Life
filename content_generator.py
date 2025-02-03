import random
import openai
from keys import OPENAI_API_KEY
from topics import topics  # Импорт списка тем
from logger import log_warning, log_error
from content_improvements.trend_analyzer import get_trending_topics
from content_improvements.prompt_optimizer import optimize_prompt
from content_improvements.duplicate_checker import is_duplicate_post, add_post_to_history
from content_improvements.spell_checker import correct_text

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
    """✍️ Генерация поста через OpenAI с разными форматами контента, с учетом трендов и проверки на ошибки."""
    if topic is None:
        topic = get_next_topic()

    trending_topics = get_trending_topics()
    topic = topic if not trending_topics else f"{topic} ({random.choice(trending_topics)})"

    # 🔹 Выбираем случайный формат поста
    post_type = random.choice(["storytelling", "checklist", "advice"])
    base_prompt = (
        "Напиши полезный и мотивирующий текст на тему: \"{topic}\". "
        "Тон — дружелюбный, мотивирующий, без лишней воды. "
        "Добавь полезные советы и короткие выводы. "
        "Объем — до 2000 символов."
    )

    prompt = optimize_prompt(base_prompt, topic)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            timeout=30
        )
        post_text = response["choices"][0]["message"]["content"].strip()
        post_text = correct_text(post_text)  # ✅ Проверяем и исправляем ошибки

        if is_duplicate_post(post_text):  # ✅ Проверяем на дубли
            return "Этот пост уже публиковался, генерируем новый..."

        add_post_to_history(post_text)  # ✅ Добавляем пост в историю
        return post_text

    except openai.error.Timeout:
        log_warning("⏳ OpenAI API слишком долго отвечает. Пропускаем этот запрос.")
        return "Ошибка генерации поста. Попробуйте позже."

    except Exception as e:
        log_error(f"❌ Ошибка при генерации текста через OpenAI: {e}")
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

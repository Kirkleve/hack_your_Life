import random
import openai
from keys import OPENAI_API_KEY
from topics import topics  # Импорт списка тем
from logger import log_warning, log_error

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
    """✍️ Генерация поста через OpenAI с разными форматами контента."""

    if topic is None:
        topic = get_next_topic()

    # 🔹 Выбираем случайный формат поста
    post_type = random.choice(["storytelling", "checklist", "advice"])

    if post_type == "storytelling":
        prompt = (
            f"Напиши вдохновляющую мини-историю на тему: \"{topic}\". "
            "Добавь интересного персонажа или реальный случай, не связанный со мной. "
            "Тон — живой, увлекательный, будто рассказываешь другу. "
            "В конце сделай вывод, который вдохновляет читателя. "
            "Структура: \n\n- Заголовок темы\n- История\n- Вывод\n- Один хэштег. "
            "Добавь 1-2 эмодзи для акцента, но без перегруза. "
            "Объём — до 2000 символов."
        )

    elif post_type == "checklist":
        prompt = (
            f"Создай практичный чек-лист по теме: \"{topic}\". "
            "Заголовок должен чётко отражать тему. "
            "Список должен содержать 5-7 пунктов с короткими, чёткими действиями. "
            "Формат:\n\n- Заголовок темы\n- Короткое вводное предложение\n- Чек-лист\n- Один хэштег. "
            "Используй эмодзи ✔ для чек-листа, но не перебарщивай. "
            "Объём — до 1500 символов."
        )

    elif post_type == "advice":
        prompt = (
            f"Напиши полезный совет на тему: \"{topic}\". "
            "Используй чёткие рекомендации и научные обоснования. "
            "Тон — уверенный, но дружелюбный. "
            "Структура: \n\n- Заголовок темы\n- Основная мысль\n- 3-5 ключевых пунктов с пояснениями"
            "\n- Заключение\n- Один хэштег. "
            "Добавь 1-2 эмодзи, чтобы выделить важное, но без перебора. "
            "Объём — до 1800 символов."
        )

    else:
        prompt = f"Напиши полезную статью на тему: \"{topic}\" с чёткой структурой и без ошибок."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            timeout=30
        )
        return format_text(response["choices"][0]["message"]["content"].strip(), post_type)

    except openai.error.Timeout:
        log_warning("⏳ OpenAI API слишком долго отвечает. Пропускаем этот запрос.")
        return "Ошибка генерации поста. Попробуйте позже."

    except Exception as e:
        log_error(f"❌ Ошибка при генерации текста через OpenAI: {e}")
        return "Ошибка генерации поста."


def format_text(text, post_type):
    """📌 Форматируем текст в зависимости от типа поста."""
    text = text.strip()

    # ✅ Делаем чек-листы удобочитаемыми
    if post_type == "checklist":
        text = text.replace("\n- ", "\n✔ ")

        # ✅ Убираем лишние пустые строки
    text = "\n".join(line.strip() for line in text.split("\n") if line.strip())

    return text


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

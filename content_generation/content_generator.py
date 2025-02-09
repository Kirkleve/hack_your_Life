"""
Файл отвечает за создание постов с помощью OpenAI, обработку и форматирование текста перед публикацией.

🔹 Генерация постов: Запрос к GPT-3.5 Turbo с учётом тематики и формата.
🔹 Оптимизация промптов: Улучшение запросов перед отправкой в OpenAI.
🔹 Проверка дубликатов: Исключение повторяющегося контента.
🔹 Исправление ошибок: Автоматическая коррекция орфографии и пунктуации.
🔹 Логирование и обработка ошибок: Запись ошибок при работе с API.
🔹 Форматирование текста: Улучшение читаемости перед публикацией в Telegram.
"""

import openai
from keys import OPENAI_API_KEY
from content_generation.formats import get_post_prompt
from content_generation.topic_manager import get_next_topic
from content_generation.text_processor import split_text_by_paragraphs  # 📌 Импорт обработки текста
from content_improvements.prompt_optimizer import optimize_prompt
from content_improvements.duplicate_checker import is_duplicate_post, add_post_to_history
from content_improvements.spell_checker import correct_text
from logger import log_warning, log_error

# ✅ Устанавливаем API-ключ для OpenAI
openai.api_key = OPENAI_API_KEY


async def generate_post(topic=None):
    """✍️ Генерация поста через OpenAI с разными форматами контента."""
    if topic is None:
        topic = get_next_topic()

    base_prompt = get_post_prompt(topic)
    prompt = await optimize_prompt(base_prompt, topic)

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            timeout=30
        )
        post_text = response["choices"][0]["message"]["content"].strip()
        post_text = correct_text(post_text)  # ✅ Проверяем и исправляем ошибки

        if is_duplicate_post(post_text):  # ✅ Проверяем на дубли
            return "Этот пост уже публиковался, генерируем новый..."

        add_post_to_history(post_text)  # ✅ Добавляем пост в историю
        return split_text_by_paragraphs(post_text)  # ✅ Теперь текст сразу форматируется перед публикацией

    except openai.error.Timeout:
        log_warning("⏳ OpenAI API слишком долго отвечает. Пропускаем этот запрос.")
        return "Ошибка генерации поста. Попробуйте позже."

    except Exception as e:
        log_error(f"❌ Ошибка при генерации текста через OpenAI: {e}")
        return "Ошибка генерации поста."

import openai
from keys import OPENAI_API_KEY
from logger import log_info, log_error


def generate_search_keywords(query):
    """🔍 AI-оптимизация запроса для поиска изображений"""
    prompt = f"""
    Улучши поисковый запрос для поиска изображений. Добавь синонимы, уточняющие слова,
    но сохрани смысл. Не добавляй лишние слова, только те, что помогают найти качественное изображение.

    Оригинальный запрос: "{query}"
    Оптимизированный запрос:
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            api_key=OPENAI_API_KEY
        )
        improved_query = response["choices"][0]["message"]["content"].strip()
        log_info(f"🔍 AI-оптимизированный запрос: {improved_query}")
        return improved_query

    except Exception as e:
        log_error(f"❌ Ошибка AI-оптимизации запроса: {e}")
        return query  # Если ошибка, используем оригинальный запрос

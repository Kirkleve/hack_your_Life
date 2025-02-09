"""
Файл отвечает за поиск изображений через Google Custom Search API.

🔹 Формирование запроса: Добавляет `-face`, чтобы исключить изображения с лицами.
🔹 Запрос к Google API: Использует ключи `GOOGLE_API_KEY` и `SEARCH_ENGINE_ID`.
🔹 Фильтрация изображений: Проверяет, не содержит ли изображение лиц и не является ли дубликатом.
🔹 Кэширование: Сохраняет найденные изображения, чтобы избежать повторного поиска.
🔹 Логирование: Фиксирует успешные находки и ошибки при запросе.
"""

import requests
from image.image_cache import is_duplicate, cache_image
from image.image_filter import get_image_hash, contains_faces
from keys import GOOGLE_API_KEY, SEARCH_ENGINE_ID
from logger import log_info, log_error


def search_image_google(query):
    """🔍 Поиск изображения через Google"""
    query = f"{query} -face"
    url = (
        f"https://www.googleapis.com/customsearch/v1?q={query}"
        f"&searchType=image&imgSize=large&fileType=jpg&safe=active"
        f"&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
    )

    try:
        log_info(f"🔎 Поиск изображений в Google по запросу: {query}")
        response = requests.get(url, timeout=10)
        data = response.json()

        for item in data.get("items", []):
            image_url = item["link"]
            image_hash = get_image_hash(image_url)

            if image_hash and not is_duplicate(image_url) and not contains_faces(image_url):
                cache_image(image_url, image_hash)
                log_info(f"✅ Найдено изображение (Google): {image_url}")
                return image_url

    except Exception as e:
        log_error(f"❌ Ошибка при поиске изображения в Google: {e}")

    return None

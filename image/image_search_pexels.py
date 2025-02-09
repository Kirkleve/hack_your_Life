"""
Файл отвечает за поиск изображений через Pexels API.

🔹 Формирование запроса: Ищет изображения по ключевым словам через Pexels API.
🔹 Фильтрация изображений: Исключает дубликаты и изображения с лицами.
🔹 Кэширование: Сохраняет найденные изображения, чтобы избежать повторных запросов.
🔹 Логирование: Записывает успешные находки и ошибки при загрузке.
"""

import requests
from image.image_cache import is_duplicate, cache_image
from image.image_filter import get_image_hash, contains_faces
from keys import PEXELS_API_KEY
from logger import log_info, log_error


def search_image_pexels(query):
    """🔍 Поиск изображения через Pexels"""
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=10"
    headers = {"Authorization": PEXELS_API_KEY}

    try:
        log_info(f"🔎 Поиск изображений в Pexels по запросу: {query}")
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        for item in data.get("photos", []):
            image_url = item["src"]["large"]
            image_hash = get_image_hash(image_url)

            if image_hash and not is_duplicate(image_url) and not contains_faces(image_url):
                cache_image(image_url, image_hash)
                log_info(f"✅ Найдено изображение (Pexels): {image_url}")
                return image_url

    except Exception as e:
        log_error(f"❌ Ошибка при поиске изображения в Pexels: {e}")

    return None

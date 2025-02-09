"""
Файл отвечает за поиск изображений через Unsplash API.

🔹 Запрос к Unsplash API: Отправляет поисковый запрос и получает 10 изображений.
🔹 Фильтрация изображений: Проверяет дубликаты и исключает фото с лицами.
🔹 Кэширование: Сохраняет найденные изображения для предотвращения повторов.
🔹 Логирование: Записывает успешные находки и ошибки при запросе.
"""


import requests
from image.image_cache import is_duplicate, cache_image
from image.image_filter import get_image_hash, contains_faces
from keys import UNSPLASH_API_KEY
from logger import log_info, log_error


def search_image_unsplash(query):
    """🔍 Поиск изображения через Unsplash"""
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=10"
    headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}

    try:
        log_info(f"🔎 Поиск изображений в Unsplash по запросу: {query}")
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        for item in data.get("results", []):
            image_url = item["urls"]["regular"]
            image_hash = get_image_hash(image_url)

            if image_hash and not is_duplicate(image_url) and not contains_faces(image_url):
                cache_image(image_url, image_hash)
                log_info(f"✅ Найдено изображение (Unsplash): {image_url}")
                return image_url

    except Exception as e:
        log_error(f"❌ Ошибка при поиске изображения в Unsplash: {e}")

    return None

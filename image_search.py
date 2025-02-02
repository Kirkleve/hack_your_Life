import requests
from image_cache import is_duplicate, cache_image
from image_filter import get_image_hash, contains_faces
from keys import PEXELS_API_KEY, GOOGLE_API_KEY, SEARCH_ENGINE_ID


def search_image_google(query):
    """🔍 Поиск изображения через Google"""
    query = f"{query} -face"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}" \
          f"&searchType=image&imgSize=large&fileType=jpg&safe=active&key={GOOGLE_API_KEY}" \
          f"&cx={SEARCH_ENGINE_ID}"
    try:
        print(f"🔎 Поиск изображений по запросу: {query}")
        response = requests.get(url, timeout=10)
        data = response.json()
        print(f"📩 Ответ Google API: {data}")
        for item in data.get("items", []):
            image_url = item["link"]
            image_hash = get_image_hash(image_url)

            if image_hash and not is_duplicate(image_url) and not contains_faces(image_url):
                cache_image(image_url, image_hash)
                print(f"✅ Изображение найдено: {image_url}")
                return image_url
    except Exception as e:
        print(f"Ошибка при поиске изображения в Google: {e}")
    return None


def search_image_pexels(query):
    """🔍 Поиск изображения через Pexels"""
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=10"
    headers = {"Authorization": PEXELS_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        print(f"📩 Ответ Pexels API: {data}")

        for item in data.get("photos", []):
            image_url = item["src"]["large"]
            image_hash = get_image_hash(image_url)

            if image_hash and not is_duplicate(image_url) and not contains_faces(image_url):
                cache_image(image_url, image_hash)
                return image_url
    except Exception as e:
        print(f"Ошибка при поиске изображения в Pexels: {e}")
    return None

import os
import json

# 📂 Теперь кэш хранится в `image/image_cache.json`
CACHE_FILE = os.path.join(os.path.dirname(__file__), "image_cache.json")


def clear_cache():
    """❌ Удаляет кэш изображений перед перезапуском"""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print("🗑 Кэш изображений очищен!")


def load_cache():
    """📂 Загружаем кэш изображений"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    return {}


def save_cache(cache):
    """💾 Сохраняем кэш изображений"""
    with open(CACHE_FILE, "w") as file:
        json.dump(cache, file)


def is_duplicate(image_url):
    """🔄 Проверяем, использовалось ли изображение ранее"""
    cache = load_cache()
    return image_url in cache


def cache_image(image_url, image_hash):
    """📝 Добавляем изображение в кэш"""
    cache = load_cache()
    cache[image_url] = image_hash
    save_cache(cache)

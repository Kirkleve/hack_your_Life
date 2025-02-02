import os
import json

CACHE_FILE = "image_cache.json"
def clear_cache():
    """❌ Удаляет кэш изображений перед перезапуском"""
    if os.path.exists("image_cache.json"):
        os.remove("image_cache.json")
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

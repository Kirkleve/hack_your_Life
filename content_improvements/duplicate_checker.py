import json
import os

CACHE_FILE = "content_improvements/post_history.json"

def load_post_history():
    """📂 Загружает историю постов."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    return []

def save_post_history(history):
    """💾 Сохраняет историю постов."""
    with open(CACHE_FILE, "w") as file:
        json.dump(history, file)

def is_duplicate_post(new_post):
    """🔄 Проверяет, был ли уже опубликован этот пост."""
    history = load_post_history()
    return new_post in history

def add_post_to_history(new_post):
    """✅ Добавляет пост в историю."""
    history = load_post_history()
    history.append(new_post)
    save_post_history(history)

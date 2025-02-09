"""
Файл отвечает за поиск изображений по ключевым словам.

🔹 Использует Google и Pexels API: Поиск изображений через два источника.
🔹 Приоритет Google: Сначала проверяет Google, затем Pexels.
🔹 Возвращает URL найденного изображения или `None`, если ничего не найдено.
"""


from image.image_search import search_image_google, search_image_pexels


def fetch_image(query):
    """🔍 Основная функция для поиска изображения"""
    image_url = search_image_google(query)
    if not image_url:
        image_url = search_image_pexels(query)
    return image_url

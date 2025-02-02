from image_search import search_image_google, search_image_pexels


def fetch_image(query):
    """🔍 Основная функция для поиска изображения"""
    image_url = search_image_google(query)
    if not image_url:
        image_url = search_image_pexels(query)
    return image_url

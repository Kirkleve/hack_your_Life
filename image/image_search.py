import concurrent.futures
from image.image_search_google import search_image_google
from image.image_search_pexels import search_image_pexels
from image.image_search_unsplash import search_image_unsplash
from image.keyword_extractor import generate_search_keywords
from logger import log_info


def search_image(query):
    """🔍 Параллельный поиск изображения с AI-оптимизированным запросом"""
    optimized_query = generate_search_keywords(query)  # AI улучшает запрос

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(search_image_google, optimized_query): "Google",
            executor.submit(search_image_pexels, optimized_query): "Pexels",
            executor.submit(search_image_unsplash, optimized_query): "Unsplash",
        }

        for future in concurrent.futures.as_completed(futures):
            source = futures[future]
            try:
                result = future.result()
                if result:
                    log_info(f"✅ Найдено изображение ({source}): {result}")
                    return result  # Возвращаем первый найденный результат
            except Exception as e:
                log_info(f"❌ Ошибка в {source}: {e}")

    log_info("⚠️ Изображение не найдено во всех сервисах.")
    return None

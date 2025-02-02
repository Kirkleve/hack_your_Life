import spacy

# Загружаем модель для обработки текста с помощью spaCy
nlp = spacy.load("ru_core_news_lg")

# Словарь синонимов для ключевых тем, включая бег и горные виды спорта
synonyms = {
    "morning": ["утро", "завтрак", "начало дня", "утренний", "утреннее время"],
    "energy": ["энергия", "жизненные силы", "активность", "энергичный", "вдохновение"],
    "motivation": ["мотивация", "цель", "настрой", "стремление", "желание"],
    "health": ["здоровье", "физическое состояние", "благополучие", "физкультура", "биохакинг"],
    "fitness": ["спорт", "фитнес", "тренировки", "упражнения", "физическая активность"],
    "productivity": ["продуктивность", "эффективность", "результативность", "цели", "планирование"],
    "habit": ["привычка", "ежедневные действия", "рутина", "ритуал"],
    "nature": ["природа", "окружающая среда", "ландшафт", "пейзаж", "ландшафт"],
    "running": ["бег", "марафон", "кросс", "дистанция", "спортсмен", "беговые тренировки"],
    "mountains": ["горы", "горный туризм", "альпинизм", "поход", "горы на высоте", "горные тропы", "экспедиция"]
}

def extract_keywords(post_text):
    """🔑 Определение ключевых слов для поиска изображений с учётом синонимов и контекста"""

    # Применяем spaCy для анализа текста
    doc = nlp(post_text.lower())  # Приводим текст к нижнему регистру для удобства

    # Ищем ключевые темы
    keywords = []

    # Проходим по синонимам и ищем их в тексте
    for key, words in synonyms.items():
        for word in words:
            if word in post_text.lower():  # Ищем совпадение в тексте
                keywords.append(key)
                break  # Если нашли хотя бы одно совпадение, прекращаем проверку для этой темы

    # Если не нашли ключевых слов, пытаемся извлечь темы с использованием словаря
    if not keywords:
        keywords.append("nature")  # Если не нашли темы, возвращаем 'nature'

    # Возвращаем первые найденные ключевые слова
    return ", ".join(keywords[:3])  # Ограничиваем результат до 3-х ключевых тем

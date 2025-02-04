import json
import datetime
import random
from keys import reaction_data_file
from content_improvements.topics import topics  # Импорт списка тем

MIN_REACTIONS = 50  # Минимальное количество реакций для анализа популярности
REPLACE_THRESHOLD = 10  # Если тема 3 раза подряд набирает < 10 лайков — она удаляется
TREND_BOOST = 2  # Увеличение частоты публикации трендовой темы


def load_reaction_data():
    """🔍 Загрузка данных о реакциях из файла и обновление старых записей"""
    try:
        with open(reaction_data_file, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    # ✅ Проверяем, есть ли `total_likes`, `total_comments`, `total_shares`, если нет — добавляем
    for topic in data.keys():
        if "total_likes" not in data[topic]:
            data[topic]["total_likes"] = 0
        if "total_comments" not in data[topic]:
            data[topic]["total_comments"] = 0
        if "total_shares" not in data[topic]:
            data[topic]["total_shares"] = 0

    save_reaction_data(data)  # ✅ Сохраняем исправленные данные
    return data


def save_reaction_data(data):
    """💾 Сохранение обновлённых данных в файл"""
    try:
        with open(reaction_data_file, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"❌ Ошибка при сохранении данных: {e}")


def update_reaction_data(topic, likes, comments, shares):
    """📊 Обновление статистики популярности тем с учётом даты"""
    data = load_reaction_data()
    today = datetime.date.today().isoformat()

    if topic not in data:
        data[topic] = {"history": [], "total_likes": 0, "total_comments": 0, "total_shares": 0}

    # ✅ Добавляем новые данные
    data[topic]["history"].append({"date": today, "likes": likes, "comments": comments, "shares": shares})
    data[topic]["total_likes"] += likes
    data[topic]["total_comments"] += comments
    data[topic]["total_shares"] += shares

    # ✅ Храним историю только за последние 7 дней
    data[topic]["history"] = [entry for entry in data[topic]["history"] if
                              (datetime.date.today() - datetime.date.fromisoformat(entry["date"])).days <= 7]

    save_reaction_data(data)


def get_most_popular_topic():
    """📢 Определение самой популярной темы с учётом трендов"""
    data = load_reaction_data()

    # ✅ Если данных нет или мало реакций — выбираем случайную тему
    if not data or sum(topic["total_likes"] + topic["total_comments"] + topic["total_shares"] for topic in
                       data.values()) < MIN_REACTIONS:
        return random.choice(topics)  # Теперь берём случайную тему вместо первой

    # ✅ Сортируем темы по популярности
    sorted_topics = sorted(data.items(), key=lambda x: (
            x[1]["total_likes"] + x[1]["total_comments"] + x[1]["total_shares"]
    ), reverse=True)

    # ✅ Если тема резко выросла в популярности за 3 дня — приоритет ей
    trending_topics = [topic for topic, stats in sorted_topics if
                       len(stats["history"]) >= 3 and
                       stats["history"][-1]["likes"] > stats["history"][-3]["likes"] * TREND_BOOST]

    return trending_topics[0] if trending_topics else sorted_topics[0][0]


def replace_least_popular_topic():
    """🔄 Заменяет самую непопулярную тему, если она стабильно неинтересна"""
    data = load_reaction_data()
    if not data:
        return  # Если данных нет, ничего не заменяем

    # ✅ Ищем темы, которые стабильно набирали мало лайков
    least_popular_topics = [topic for topic, stats in data.items() if
                            len(stats["history"]) >= 3 and
                            all(entry["likes"] < REPLACE_THRESHOLD for entry in stats["history"][-3:])]

    if least_popular_topics:
        topic_to_remove = least_popular_topics[0]
        new_topic = next((t for t in topics if t not in data), None)

        if new_topic:
            print(f"🔄 Заменяем тему '{topic_to_remove}' на '{new_topic}'")
            del data[topic_to_remove]  # Удаляем старую тему
            data[new_topic] = {"history": [], "total_likes": 0, "total_comments": 0,
                               "total_shares": 0}  # Добавляем новую
            save_reaction_data(data)

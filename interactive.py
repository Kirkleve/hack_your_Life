from telegram import Bot
from keys import TELEGRAM_BOT_TOKEN, CHAT_ID
import random
import asyncio
from analytics import get_most_popular_topic, load_reaction_data

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# ✅ Персонализированные опросы (бот выбирает тему, которая нравится подписчикам)
async def send_poll():
    """📊 Отправка персонализированного опроса в канал"""
    topic = get_most_popular_topic()  # ✅ Получаем самую популярную тему
    question = f"Какую тему ты хочешь видеть чаще?"
    options = ["Спорт", "Продуктивность", "Биохакинг", "Здоровье"]

    # ✅ Если бот видит, что подписчики больше лайкают посты про спорт, он подбирает спорт-тематику
    if "спорт" in topic.lower():
        question = "Какой вид спорта тебе интересен больше всего?"
        options = ["Бег", "Фитнес", "Плавание", "Йога"]

    try:
        await bot.send_poll(chat_id=CHAT_ID, question=question, options=options)
        await asyncio.sleep(5)
    except Exception as e:
        print(f"❌ Ошибка при отправке опроса: {e}")


# ✅ Викторины с разными уровнями сложности
async def send_quiz():
    """🧠 Отправка викторины в канал (Теперь всегда анонимно)"""
    reaction_data = load_reaction_data()  # Загружаем данные о реакциях

    # ✅ Фильтруем данные, чтобы убрать возможные списки (берём только int)
    total_reactions = sum(
        sum(value for value in topic.values() if isinstance(value, int))
        for topic in reaction_data.values()
    )

    # Если подписчики активно реагируют, даём сложный вопрос
    if total_reactions > 100:
        question = "Какой элемент питания даёт наибольшую энергию?"
        options = ["Белки", "Жиры", "Углеводы", "Минералы"]
        correct_option_id = 2  # ✅ "Углеводы"

    else:
        question = "Какой продукт содержит больше всего витамина C?"
        options = ["Лимон", "Киви", "Перец", "Апельсин"]
        correct_option_id = 1  # ✅ "Киви"

    try:
        await bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=True  # ✅ Теперь опрос всегда анонимный (чтобы не было ошибки)
        )
        await asyncio.sleep(5)
    except Exception as e:
        print(f"❌ Ошибка при отправке викторины: {e}")




# ✅ Улучшенная система челленджей с напоминаниями
active_challenge = None  # Храним активный челлендж

async def send_challenge_day():
    """🔥 Отправка челленджа дня + напоминание, если он не выполнен"""
    global active_challenge
    challenges = [
        "💪 День 1: 50 приседаний",
        "🏃 День 2: 10 минут бега",
        "📖 День 3: Прочитать 5 страниц книги",
        "💧 День 4: Выпить 2 литра воды",
        "🧘 День 5: 5 минут медитации"
    ]

    # ✅ Если челлендж уже был отправлен и не выполнен – напоминаем о нём
    if active_challenge:
        try:
            await bot.send_message(chat_id=CHAT_ID, text=f"⏳ Не забывай про текущий челлендж: {active_challenge}")
        except Exception as e:
            print(f"❌ Ошибка при отправке напоминания о челлендже: {e}")
        return  # Не отправляем новый челлендж

    active_challenge = random.choice(challenges)

    try:
        await bot.send_message(chat_id=CHAT_ID, text=f"🔥 Челлендж дня: {active_challenge}")
        await asyncio.sleep(5)
    except Exception as e:
        print(f"❌ Ошибка при отправке челленджа: {e}")


# ✅ Итог недели с анализом активности подписчиков
async def send_weekly_summary():
    """📅 Подведение итогов недели с реальными данными"""
    reaction_data = load_reaction_data()
    most_liked_topic = max(reaction_data, key=lambda topic: reaction_data[topic]["total_likes"], default="Нет данных")

    summary_text = (
        "📝 Итоги недели:\n"
        f"✔ Самая популярная тема: {most_liked_topic}\n"
        f"🔥 Количество реакций: {sum(topic['total_likes'] for topic in reaction_data.values())}\n"
        f"🏆 Лучший подписчик: @username (по лайкам)"
    )

    try:
        await bot.send_message(chat_id=CHAT_ID, text=summary_text)
        await asyncio.sleep(5)
    except Exception as e:
        print(f"❌ Ошибка при отправке недельного отчёта: {e}")


# ✅ Обратная связь с подписчиками (теперь на основе их предпочтений)
async def send_feedback_request():
    """💬 Запрос обратной связи на основе активности подписчиков"""
    topic = get_most_popular_topic()
    feedback_text = f"💬 Что вам больше всего понравилось в постах про {topic}? Напишите нам!"

    try:
        await bot.send_message(chat_id=CHAT_ID, text=feedback_text)
    except Exception as e:
        print(f"❌ Ошибка при запросе обратной связи: {e}")

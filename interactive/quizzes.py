import random
from telegram import Bot
from keys import TELEGRAM_BOT_TOKEN, CHAT_ID
import asyncio
from logger import log_info, log_error

bot = Bot(token=TELEGRAM_BOT_TOKEN)

quiz_questions = [
    {
        "question": "Какой гормон называют 'гормоном счастья'?",
        "options": ["Дофамин", "Адреналин", "Кортизол", "Мелатонин"],
        "correct_index": 0,
        "explanation": "Дофамин отвечает за мотивацию, удовольствие и радость. 😊"
    },
    {
        "question": "Какое время суток лучше всего для тренировок?",
        "options": ["Утро", "День", "Вечер", "Когда удобно"],
        "correct_index": 3,
        "explanation": "Главное — стабильность. Если тренироваться регулярно, организм адаптируется!"
    },
    {
        "question": "Какой витамин важен для крепких костей?",
        "options": ["Витамин C", "Витамин A", "Витамин D", "Витамин B12"],
        "correct_index": 2,
        "explanation": "Витамин D способствует усвоению кальция, который необходим для костей."
    },
    {
        "question": "Какой напиток помогает ускорить обмен веществ?",
        "options": ["Сладкий чай", "Кофе", "Газировка", "Тёплая вода с лимоном"],
        "correct_index": 1,
        "explanation": "Кофеин в кофе стимулирует обмен веществ и повышает уровень энергии. ☕"
    },
    {
        "question": "Какой тип дыхания помогает быстрее успокоиться?",
        "options": ["Глубокое дыхание", "Поверхностное дыхание", "Частое дыхание", "Дыхание через рот"],
        "correct_index": 0,
        "explanation": "Глубокое дыхание снижает уровень стресса и помогает расслабиться. 🧘"
    }
]

used_questions = []  # ✅ Список использованных вопросов

async def send_quiz():
    """🧠 Отправка викторины с правильным ответом и объяснением"""
    global used_questions

    # 🔄 Если все вопросы использованы, сбрасываем список
    if len(used_questions) == len(quiz_questions):
        used_questions = []

    # 🔍 Выбираем случайный вопрос, который ещё не использовался
    available_questions = [q for q in quiz_questions if q not in used_questions]
    question_data = random.choice(available_questions)
    used_questions.append(question_data)

    try:
        log_info(f"📤 Отправка викторины: {question_data['question']}")  # ✅ Логируем процесс

        await bot.send_poll(
            chat_id=CHAT_ID,
            question=question_data["question"],
            options=question_data["options"],
            type="quiz",
            correct_option_id=question_data["correct_index"],
            is_anonymous=True
        )

        await asyncio.sleep(60)

        explanation = f"📢 Правильный ответ: {question_data['options'][question_data['correct_index']]}\n\n💡 {question_data['explanation']}"
        await bot.send_message(chat_id=CHAT_ID, text=explanation)

    except Exception as e:
        log_error(f"❌ Ошибка при отправке викторины: {e}")

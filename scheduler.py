"""
Файл отвечает за планирование и управление расписанием публикаций бота.

🔹 Запуск первичных задач: Выполняет ключевые действия при старте (челленджи, публикации, опросы).
🔹 Настройка расписания: Определяет временные интервалы для постов, челленджей и взаимодействий.
🔹 Управление челленджами: Запускает новый челлендж в начале недели, публикует ежедневные задания.
🔹 Автоматическое выполнение задач: Использует `schedule` и `asyncio` для работы в бесконечном цикле.
🔹 Логирование: Фиксирует запуск, выполнение и возможные ошибки при работе бота.
"""

import schedule
import asyncio
# from content_improvements.trend_analyzer import get_trending_topics
from interactive.challenges.challenge_manager import check_and_start_new_challenge
from interactive.challenges.challenge_poster import post_challenge
from telegram_bot import post_to_telegram
from interactive.tasks import send_poll, send_quiz, send_weekly_summary, \
    send_feedback_request
from logger import log_info


async def run_initial_tasks():
    """✅ Выполняет все задачи при старте проекта с актуальными трендами"""
    log_info("🚀 Получаем актуальные тренды перед запуском...")

    # trending_topics = await get_trending_topics()  # ✅ Исправленный вызов
    # log_info(f"📊 Тренды загружены: {trending_topics[:5]}")  # ✅ Логируем топ-5 трендов

    #await post_to_telegram()
    #await asyncio.sleep(10)

    #await send_poll()
    #await asyncio.sleep(10)

    #await post_to_telegram()
    #await asyncio.sleep(10)

    #await send_quiz()
    #await asyncio.sleep(10)
    check_and_start_new_challenge()  # Проверка и запуск челленджа, если нужно
    await asyncio.sleep(5)

    await post_challenge()  # Публикация текущего задания челленджа
    await asyncio.sleep(10)

    await send_weekly_summary()
    await asyncio.sleep(10)

    await send_feedback_request()

    log_info("✅ Первичная проверка завершена. Переход к стандартному расписанию.")


def schedule_posts():
    """📅 Настройка стандартного расписания публикаций"""
    schedule.every().day.at("08:00").do(lambda: asyncio.create_task(post_to_telegram()))
    schedule.every().day.at("12:00").do(lambda: asyncio.create_task(send_poll()))
    schedule.every().day.at("15:00").do(lambda: asyncio.create_task(post_to_telegram()))
    schedule.every().day.at("18:00").do(lambda: asyncio.create_task(send_quiz()))

    schedule.every().monday.at("08:00").do(
        lambda: asyncio.create_task(check_and_start_new_challenge()))  # Запуск нового челленджа
    schedule.every().day.at("08:10").do(
        lambda: asyncio.create_task(post_challenge()))  # Публикация задания челленджа

    schedule.every().monday.at("09:00").do(lambda: asyncio.create_task(send_weekly_summary()))
    schedule.every().friday.at("19:00").do(lambda: asyncio.create_task(send_feedback_request()))


async def run_schedule():
    """♻ Бесконечный цикл выполнения задач"""
    await run_initial_tasks()  # ✅ Сначала выполняем все задачи сразу

    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

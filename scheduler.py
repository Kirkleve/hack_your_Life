import schedule
import asyncio
from content_improvements.trend_analyzer import get_trending_topics
from telegram_bot import post_to_telegram
from interactive.tasks import send_poll, send_quiz, send_challenge_day, send_weekly_summary, send_feedback_request
from logger import log_info


async def run_initial_tasks():
    """✅ Выполняет все задачи при старте проекта с актуальными трендами"""
    log_info("🚀 Получаем актуальные тренды перед запуском...")

    # trending_topics = await get_trending_topics()  # ✅ Исправленный вызов
    # log_info(f"📊 Тренды загружены: {trending_topics[:5]}")  # ✅ Логируем топ-5 трендов

    await post_to_telegram()
    await asyncio.sleep(10)

    await send_poll()
    await asyncio.sleep(10)

    await post_to_telegram()
    await asyncio.sleep(10)

    await send_quiz()
    await asyncio.sleep(10)

    await send_challenge_day()
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
    schedule.every().day.at("20:00").do(lambda: asyncio.create_task(send_challenge_day()))

    schedule.every().monday.at("09:00").do(lambda: asyncio.create_task(send_weekly_summary()))
    schedule.every().friday.at("19:00").do(lambda: asyncio.create_task(send_feedback_request()))


async def run_schedule():
    """♻ Бесконечный цикл выполнения задач"""
    await run_initial_tasks()  # ✅ Сначала выполняем все задачи сразу

    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

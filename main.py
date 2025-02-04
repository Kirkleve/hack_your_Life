import asyncio
from scheduler import run_schedule
# from telethon import TelegramClient  # 🔹 Временно отключаем Telegram API
from keys import API_ID, API_HASH
from logger import log_critical, log_info  # ✅ Импортируем логирование

SESSION_FILE = "trend_analyzer_session"
# client = TelegramClient(SESSION_FILE, API_ID, API_HASH)  # 🔹 Временно отключаем Telegram API

async def main():
    """🚀 Запускает бота и обновляет тренды перед стартом"""
    print("🚀 Запуск бота")

    # log_info("📊 Получаем тренды...")
    # trending_topics = await get_trending_topics()  # 🔹 Временно отключаем Telegram API
    # log_info(f"📊 Загружены тренды: {trending_topics[:5]}")  # 🔹 Временно отключаем Telegram API

    while True:
        try:
            log_info("📅 Запускаем планировщик...")
            asyncio.create_task(run_schedule())
            await asyncio.sleep(3600)
        except Exception as e:
            log_critical(f"❌ Ошибка в работе бота: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    while True:
        try:
            loop.run_until_complete(main())
        except Exception as e:
            log_critical(f"❗ Критическая ошибка, перезапуск: {e}")
            asyncio.sleep(5)

import asyncio

from scheduler import run_schedule
from logger import log_critical  # ✅ Импортируем логирование


async def main():
    """🚀 Запускает бота и планировщик в бесконечном цикле с авто-перезапуском"""
    print("🚀 Бот запущен!")
    while True:
        try:
            asyncio.create_task(run_schedule())
            await asyncio.sleep(3600)
        except Exception as e:
            log_critical(f"❌ Ошибка в работе бота: {e}")
            await asyncio.sleep(10)  # 🔄 Перезапуск через 10 секунд

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

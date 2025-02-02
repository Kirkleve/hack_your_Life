import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram.request import HTTPXRequest
from keys import TELEGRAM_BOT_TOKEN, CHAT_ID
from image.image_fetcher import fetch_image
from content_generator import generate_post, split_text_by_paragraphs
from analytics import get_most_popular_topic
from handlers import handle_mention, handle_reactions
from image.keyword_extractor import extract_keywords
from logger import log_info, log_warning, log_error  # ✅ Импортируем логирование

# ✅ Оптимизированный пул соединений для Telegram API
request = HTTPXRequest(pool_timeout=30)
bot = Bot(token=TELEGRAM_BOT_TOKEN, request=request)

# ✅ Создаём приложение Telegram
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mention))
application.add_handler(MessageHandler(filters.ALL, handle_reactions))


async def post_to_telegram():
    """📢 Публикация поста в Telegram: Картинка + заголовок, затем раскрытие темы"""

    # ✅ Получаем актуальную тему поста
    popular_topic = get_most_popular_topic()
    post_text = generate_post(topic=popular_topic)

    # ✅ Разделяем текст на заголовок и основную часть
    title, body_parts = split_text_by_paragraphs(post_text)

    # ✅ Подбираем изображение по ключевым словам
    query = extract_keywords(title)
    image_url = fetch_image(f"{query} site:pinterest.com")

    if not image_url:
        log_warning("⚠️ Ни один источник не дал изображения!")

    full_body = ""

    try:
        if image_url and image_url.startswith("http"):
            log_info(f"📤 Отправка изображения: {image_url}")
            await bot.send_photo(chat_id=CHAT_ID, photo=image_url, caption=title)
            await asyncio.sleep(10)  # ✅ Увеличиваем паузу перед текстом
            log_info(f"📸 Отправлено фото по теме: {popular_topic}")
        else:
            log_warning(f"⚠️ Изображение не найдено или некорректное: {image_url}")
            await bot.send_message(chat_id=CHAT_ID, text=title)
            log_warning(f"📝 Отправлен заголовок без фото: {popular_topic}")

        await asyncio.sleep(10)  # ✅ Увеличили задержку

        full_body = "\n\n".join(body_parts)
        if len(full_body) > 4096:
            full_body = full_body[:4093] + "..."

        await bot.send_message(chat_id=CHAT_ID, text=full_body)
        log_info(f"✅ Отправлен пост по теме: {popular_topic}")

    except Exception as e:
        log_error(f"❌ Ошибка при отправке поста: {e}")

        if "Pool timeout" in str(e):
            log_warning("⚠️ Пропускаем повторную попытку из-за ошибки Pool timeout")
            return

        await asyncio.sleep(10)

        try:
            if image_url and image_url.startswith("http"):
                log_info(f"📤 Повторная отправка изображения: {image_url}")
                await bot.send_photo(chat_id=CHAT_ID, photo=image_url, caption=title)
            else:
                await bot.send_message(chat_id=CHAT_ID, text=title)

            await asyncio.sleep(5)
            await bot.send_message(chat_id=CHAT_ID, text=full_body)
            log_info(f"🔄 Повторно отправлен пост по теме: {popular_topic}")

        except Exception as e:
            log_error(f"⚠️ Повторная ошибка отправки поста: {e}")
            await asyncio.sleep(30)

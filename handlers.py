"""
Файл отвечает за обработку пользовательских взаимодействий в Telegram-боте.

🔹 Реакция на упоминания: Отвечает на сообщения с "@admin" и "@channel_owner".
🔹 Обновление аналитики: Фиксирует лайки, комментарии и репосты для оценки популярности тем.
🔹 Определение самой популярной темы: Анализирует, какая тема вызывает наибольший отклик.
🔹 Имитация задержки ответа: Использует `asyncio.sleep(5)`, чтобы имитировать естественное поведение бота.
"""

import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from analytics import update_reaction_data, get_most_popular_topic


async def handle_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """📢 Отвечает на упоминания в комментариях (@admin, @channel_owner)"""
    if update.message and update.message.text:
        if "@admin" in update.message.text.lower() or "@channel_owner" in update.message.text.lower():
            await asyncio.sleep(5)  # ⏳ Имитация задержки ответа
            await update.message.reply_text("🔹 Спасибо за ваш вопрос! Администратор скоро ответит. 😊")


async def handle_reactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """📊 Обновляет данные о реакциях (лайки, комментарии, репосты)"""
    if update.message:
        topic = get_most_popular_topic()
        update_reaction_data(topic, likes=1, comments=1, shares=0)  # Условное обновление данных

        # ✅ Проверяем, есть ли лайки через `Message.reply_to_message`
        if update.message.reply_to_message:
            update_reaction_data(topic, likes=2, comments=1, shares=1)  # Усиленное обновление


import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

APPS_SCRIPT_URL = os.environ[""]  # URL из шага 1

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split(maxsplit=2)

    # Заполняем что есть, остальное — пустая строка
    amount   = parts[0] if len(parts) > 0 else ""
    category = parts[1] if len(parts) > 1 else ""
    person   = parts[2] if len(parts) > 2 else ""

    requests.post(APPS_SCRIPT_URL, json={
        "amount": amount,
        "category": category,
        "person": person
    })

    # Сообщаем что именно записали
    missing = []
    if not category: missing.append("категория")
    if not person:   missing.append("кто")
    
    if missing:
        note = f" (не указано: {', '.join(missing)})"
    else:
        note = ""
    
    await update.message.reply_text(f"Готово ✅{note}")

app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()

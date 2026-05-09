from dotenv import load_dotenv
load_dotenv()

import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

APPS_SCRIPT_URL = os.environ["APPS_SCRIPT_URL"]

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split(maxsplit=2)

    amount   = parts[0] if len(parts) > 0 else ""
    category = parts[1] if len(parts) > 1 else ""
    person   = parts[2] if len(parts) > 2 else ""

    requests.post(APPS_SCRIPT_URL, json={
        "amount": amount,
        "category": category,
        "person": person
    })

    try:
        big = int(amount) > 1000
    except:
        big = False

    if not category and not person:
        comment = "ты не добавил нахера и кто, блядь, но"
    elif not category:
        comment = "ты не добавил нахера, но"
    elif not person:
        comment = "ты не добавил кто, блядь, но"
    else:
        comment = ""

    ending = "нихуя ж себе, добавил 🤑" if big else "добавил ✅"
    reply = f"{comment} {ending}".strip()
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()

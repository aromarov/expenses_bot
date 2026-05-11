from dotenv import load_dotenv
load_dotenv()
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

APPS_SCRIPT_URL = os.environ["APPS_SCRIPT_URL"]

WHO = {
    "мур": "Мурад",
    "сюм": "Расул",
    "сеня": "Арсен"
    # добавляй сколько угодно
}

WHAT = {
    "магаз": "Продукты",
    "рестик": "Ресторан",
    "магазин": "Продукты",
    "алко": "Алкоголь",
    "пиво": "Алкоголь",
    "кофе": "Кофе и закусь",
    "чай": "Кофе и закусь"
    # добавляй сколько угодно
}

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split(maxsplit=2)

    amount   = parts[0] if len(parts) > 0 else ""
    person   = parts[1] if len(parts) > 1 else ""
    category = parts[2] if len(parts) > 2 else ""

    person   = WHO.get(person.lower(), person.capitalize())
    category = WHAT.get(category.lower(), category.capitalize())

    try:
        amount_int = int(amount)
    except:
        await update.message.reply_text("это нихуя не число в начале, эй. не буду записывать")
        return

    if amount_int == 0:
        await update.message.reply_text("серьёзно? не запишу")
        return

    requests.post(APPS_SCRIPT_URL, json={
        "amount": amount,
        "person": person,
        "category": category,
    })

    big = amount_int > 1000

    if not category and not person:
        comment = "ты не написал нахера и кто, блядь, но"
    elif not category:
        comment = "ты не написал нахера, но"
    elif not person:
        comment = "ты не написал кто, блядь, но"
    else:
        comment = ""

    ending = "нихуя ж себе, добавил 🤑" if big else "добавил ✅"
    reply = f"{comment} {ending}".strip()
    await update.message.reply_text(reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("я тут, напиши сколько вы потратили 💸")

async def last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = requests.get(APPS_SCRIPT_URL, params={"action": "last"})
    await update.message.reply_text(f"последние проебы:\n{r.text}")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = requests.get(APPS_SCRIPT_URL, params={"action": "today"})
    await update.message.reply_text(f"сегодня проебано: {r.text}")

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = requests.get(APPS_SCRIPT_URL, params={"action": "total"})
    await update.message.reply_text(f"всего проебано: {r.text}")

app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("last", last))
app.add_handler(CommandHandler("today", today))
app.add_handler(CommandHandler("total", total))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()

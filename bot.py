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
        comment = "ты не добавил зачем и кто, но"
    elif not category:
        comment = "ты не добавил нахера, но"
    elif not person:
        comment = "ты не добавил кто нахуй, но"
    else:
        comment = ""

    if big:
        ending = "нихуя себе, добавил 🤑"
    else:
        ending = "добавил ✅"

    reply = f"{comment} {ending}".strip()
    await update.message.reply_text(reply)

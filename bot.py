import os
import json
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random
import json
import os

# تحميل الدول
with open("countries.json", "r", encoding="utf-8") as f:
    countries = json.load(f)

current_questions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبا 👋\n"
        "أنا لعبة العواصم 🌍\n"
        "اكتب /play لبدء اللعب"
    )

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country = random.choice(list(countries.keys()))
    capital = countries[country]["capital"]
    flag = countries[country]["flag"]

    current_questions[update.effective_user.id] = capital

    await update.message.reply_text(
        f"🌍 ما هي عاصمة {country}؟ {flag}"
    )

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in current_questions:
        return

    if update.message.text.strip() == current_questions[user_id]:
        await update.message.reply_text("✅ إجابة صحيحة!")
    else:
        await update.message.reply_text(
            f"❌ خطأ، الإجابة الصحيحة هي: {current_questions[user_id]}"
        )

    del current_questions[user_id]

def main():
    app = ApplicationBuilder().token(os.environ["8339013512:AAGnr2i2pWXB7DnQaEMvwoVu6W2Hz3HG2VU"]).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))

    app.run_polling()

if __name__ == "__main__":
    main()

import os
import json
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# قراءة جميع الدول من ملف JSON
with open("countries.json", encoding="utf-8") as f:
    countries = json.load(f)

# لتخزين الدولة الحالية لكل لاعب
current_country = {}

# لتخزين النقاط لكل لاعب
scores = {}

# أمر البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 مرحبا بك في لعبة العواصم!\n"
        "اكتب /play باش نبدأو\n"
        "اكتب /score باش تشوف نقاطك"
    )

# أمر اللعب
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country = random.choice(list(countries.keys()))
    current_country[update.effective_user.id] = country
    flag = countries[country]["flag"]  # إيموجي العلم
    
    await update.message.reply_text(
        f"🌍 ما هي عاصمة {country}? {flag}"
    )

# التحقق من الإجابة وإضافة النقاط
async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in current_country:
        await update.message.reply_text("اكتب /play باش تبدأ اللعبة 😉")
        return

    correct = countries[current_country[user_id]]["capital"]
    user_answer = update.message.text.strip()

    if user_answer == correct:
        await update.message.reply_text("✅ صح! برافو عليك 👏")
        scores[user_id] = scores.get(user_id, 0) + 1
    else:
        await update.message.reply_text(f"❌ خطأ\nالعاصمة الصحيحة هي: {correct}")

    del current_country[user_id]
    await update.message.reply_text("تحب تعاود؟ اكتب /play")

# عرض النقاط
async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_score = scores.get(user_id, 0)
    await update.message.reply_text(f"🏆 نقاطك: {user_score}")

# تشغيل البوت
def main():
   app = ApplicationBuilder().token(os.environ["TOKEN"]).build()


    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

    print("🤖 البوت راهو يخدم...")
    app.run_polling()

if __name__ == "__main__":
    main()

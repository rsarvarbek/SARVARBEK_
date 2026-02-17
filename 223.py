from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8570449532:AAF8Ieu3YBYN7S7wESvIICdcvUpN4eKYd-8"

questions = [
    {
        "question": "1️⃣ Kompyuterning asosiy qurilmasi qaysi?",
        "options": ["Monitor", "Printer", "Sistemali blok"],
        "answer": "Sistemali blok"
    },
    {
        "question": "2️⃣ CPU nima vazifani bajaradi?",
        "options": ["Ma'lumot saqlaydi", "Hisob-kitob qiladi", "Chop etadi"],
        "answer": "Hisob-kitob qiladi"
    },
    {
        "question": "3️⃣ Algoritm nima?",
        "options": [
            "Kompyuter qurilmasi",
            "Masalani yechish ketma-ketligi",
            "Dasturlash tili"
        ],
        "answer": "Masalani yechish ketma-ketligi"
    },
    {
        "question": "4️⃣ Quyidagilardan qaysi biri dasturlash tili?",
        "options": ["HTML", "Python", "Windows"],
        "answer": "Python"
    },
    {
        "question": "5️⃣ Internet nima?",
        "options": [
            "Dastur",
            "Global kompyuter tarmog‘i",
            "Operatsion sistema"
        ],
        "answer": "Global kompyuter tarmog‘i"
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["index"] = 0
    context.user_data["score"] = 0
    await send_question(update, context)

async def send_question(update, context):
    index = context.user_data["index"]
    q = questions[index]

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=opt)]
        for opt in q["options"]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(q["question"], reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text(
            q["question"], reply_markup=reply_markup
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    index = context.user_data["index"]
    correct = questions[index]["answer"]

    if query.data == correct:
        context.user_data["score"] += 1
        await query.message.reply_text("✅ To‘g‘ri!")
    else:
        await query.message.reply_text(f"❌ Noto‘g‘ri!\nTo‘g‘ri javob: {correct}")

    context.user_data["index"] += 1

    if context.user_data["index"] < len(questions):
        await send_question(update, context)
    else:
        score = context.user_data["score"]
        total = len(questions)
        await query.message.reply_text(
            f"🎉 Test yakunlandi!\n\nNatija: {score}/{total}\nFoiz: {int(score/total*100)}%"
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
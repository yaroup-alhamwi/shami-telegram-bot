import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# إعداد مفاتيح البيئة
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# دالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا وسهلا! 🖐️ احكي معي باللهجة الشامية وأنا بجاوبك بكل ود 😊")

# دالة الرد العامة
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "احكي باللهجة الشامية بطريقة ودودة وطبيعية."},
                {"role": "user", "content": user_message}
            ]
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"صار خطأ 😅: {e}")

# بناء التطبيق (ما في Updater هون)
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# ربط الأوامر والرسائل
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("✅ Bot is running and ready to chat!")
app.run_polling()

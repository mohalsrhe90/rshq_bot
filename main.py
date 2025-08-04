import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from keep_alive import keep_alive

# ✅ إعداد تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# ✅ استدعاء توكن البوت من متغيرات البيئة
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ✅ أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! أنا البوت الخاص بك ✨")

# ✅ أمر اختبار
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong!")

# ✅ التعامل مع أي رسالة نصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"أنت قلت: {update.message.text}")

# ✅ الدالة الرئيسية
def main():
    keep_alive()  # إبقاء السيرفر شغال على Render

    if not BOT_TOKEN:
        raise ValueError("❌ تأكد من أنك أضفت BOT_TOKEN في متغيرات البيئة")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

# ✅ تشغيل البرنامج
if __name__ == "__main__":
    main()

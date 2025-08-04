import logging
import os
from telegram import Update
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from telegram.error import TelegramError
from keep_alive import keep_alive

# ✅ التوكن الخاص بالبوت
BOT_TOKEN = "8419874313:AAH3csdSkAlYytsV0pEYpvzUwGabWGsryGI"

# ✅ روابط القنوات المطلوبة للاشتراك الإجباري
REQUIRED_CHANNELS = ["@Nodi39", "@tyaf90"]

# ✅ رابط Webhook الخاص بك
WEBHOOK_URL = "https://rshq-bot.onrender.com"

# ✅ تفعيل سجل الأخطاء
logging.basicConfig(level=logging.INFO)


# ✅ التحقق من اشتراك المستخدم
async def is_user_subscribed(bot, user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except TelegramError:
            return False
    return True


# ✅ الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await is_user_subscribed(context.bot, user_id):
        await update.message.reply_text("مرحبًا بك! الرجاء إرسال رابط المنشور الذي تريد إرسال التفاعلات إليه.")
        context.user_data['awaiting_post_link'] = True
    else:
        await update.message.reply_text(
            "يرجى الاشتراك في القناتين أولاً لمتابعة استخدام البوت:\n\n"
            "📢 1. @Nodi39\n"
            "📢 2. @tyaf90\n\n"
            "بعد الاشتراك، أرسل /start مرة أخرى."
        )


# ✅ معالجة الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if context.user_data.get('awaiting_post_link'):
        context.user_data['post_link'] = text
        context.user_data['awaiting_post_link'] = False
        context.user_data['awaiting_reactions'] = True
        await update.message.reply_text(
            "رائع! الآن أرسل عدد وأشكال التفاعلات التي تريدها، مفصولة بفاصلة.\n"
            "مثال: ❤️, 😂, 🔥, 👍"
        )
    elif context.user_data.get('awaiting_reactions'):
        reactions = [r.strip() for r in text.split(',') if r.strip()]
        if reactions:
            post_link = context.user_data.get('post_link')
            await update.message.reply_text(
                f"✅ تم استلام طلبك.\n"
                f"📎 المنشور: {post_link}\n"
                f"🎯 التفاعلات المطلوبة: {', '.join(reactions)}\n\n"
                f"سيتم إرسال التفاعلات لاحقًا بسبب الضغط على البوت، شكرًا لصبرك!"
            )
            context.user_data.clear()
        else:
            await update.message.reply_text("يرجى إرسال التفاعلات مفصولة بفاصلة، مثل: ❤️, 😂, 🔥, 👍")
    else:
        await update.message.reply_text("اكتب /start للبدء.")


# ✅ أمر فحص البوت
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت يعمل الآن.")


# ✅ تشغيل البوت
def main():
    keep_alive()

    app: Application = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ✅ تشغيل Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )


if __name__ == "__main__":
    main()

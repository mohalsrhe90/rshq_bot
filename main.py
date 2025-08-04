import telebot
from telebot import types
import requests

# ✅ التوكن
BOT_TOKEN = "8392401732:AAE9-KtZD-IqZGRRbxL_6YPBk1AiaAFNDjM"
bot = telebot.TeleBot(BOT_TOKEN)

# ✅ معرفات القنوات المطلوبة للاشتراك
REQUIRED_CHANNELS = ["@tyaf90", "@Nodi39"]

# ✅ رسالة الترحيب
WELCOME_MESSAGE = """
🤖 مرحبًا بك في بوت زيادة التفاعل!

📌 لاستخدام البوت، يجب أولاً الاشتراك في القنوات التالية:
- @tyaf90
- @Nodi39

✅ بعد الاشتراك، أرسل /start مجددًا.
"""

# ✅ التحقق من الاشتراك
def is_user_subscribed(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'creator', 'administrator']:
                return False
        except:
            return False
    return True

# ✅ عند استقبال /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if not is_user_subscribed(user_id):
        bot.send_message(user_id, WELCOME_MESSAGE)
        return

    msg = (
        "✅ شكراً لاشتراكك في القنوات!\n\n"
        "📌 الآن، قم بإضافة البوت كـ *أدمن في قناتك*.\n"
        "ثم أرسل رابط المنشور الذي تريد زيادة التفاعل عليه."
    )
    bot.send_message(user_id, msg, parse_mode="Markdown")

    bot.register_next_step_handler(message, get_post_link)

# ✅ بعد إرسال رابط المنشور
def get_post_link(message):
    post_link = message.text.strip()
    msg = "📊 أرسل الآن عدد التفاعلات المطلوبة (مثلاً: 100):"
    bot.send_message(message.chat.id, msg)
    bot.register_next_step_handler(message, get_reaction_count, post_link)

# ✅ بعد إرسال العدد
def get_reaction_count(message, post_link):
    try:
        count = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "❌ الرجاء إدخال رقم صحيح.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["❤️", "👍", "🔥", "😂", "💯"]
    markup.add(*buttons)

    bot.send_message(message.chat.id, "🎭 اختر شكل التفاعل:", reply_markup=markup)
    bot.register_next_step_handler(message, confirm_request, post_link, count)

# ✅ بعد اختيار شكل التفاعل
def confirm_request(message, post_link, count):
    emoji = message.text.strip()
    bot.send_message(
        message.chat.id,
        f"""✅ تم استلام الطلب بنجاح!

📌 الرابط: {post_link}
🔢 العدد المطلوب: {count}
🎭 التفاعل: {emoji}

⌛ سيتم تنفيذ التفاعل لاحقًا بسبب الضغط على البوت.
شكراً لاستخدامك البوت ❤️
""",
        reply_markup=types.ReplyKeyboardRemove()
    )

# ✅ تشغيل السيرفر للـ UptimeRobot
import keep_alive
keep_alive.keep_alive()

# ✅ بدء تشغيل البوت
bot.infinity_polling()

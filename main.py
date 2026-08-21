import os
import threading
from flask import Flask
from anthropic import Anthropic
import telebot

# إعداد خادم الويب (لإبقاء الخدمة مستيقظة)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# إعدادات البوت
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
claude = Anthropic(api_key=CLAUDE_API_KEY)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = claude.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": f"صغ إعلاناً جذاباً لـ: {message.text}"}],
        )
        bot.reply_to(message, response.content[0].text)
    except Exception as e:
        bot.reply_to(message, "حدث خطأ.")

if __name__ == "__main__":
    # تشغيل Flask في Thread منفصل
    threading.Thread(target=run_flask).start()
    # تشغيل البوت
    bot.infinity_polling()

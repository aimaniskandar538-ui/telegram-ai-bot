import os
import threading
from flask import Flask
import google.generativeai as genai
import telebot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(f"أنت مساعد تسويقي محترف. صغ إعلاناً جذاباً بناءً على الطلب: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {str(e)[:100]}")

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()

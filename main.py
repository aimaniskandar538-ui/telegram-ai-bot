import os
import threading
from flask import Flask
import google.generativeai as genai
import telebot

app = Flask(__name__)


@app.route('/')
def home():
  return 'Bot is alive!'


def run_flask():
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# تهيئة المكتبة والنموذج
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    prompt = (
        'أنت مساعد تسويقي محترف للمتاجر. صغ إعلاناً جذاباً بناءً على الطلب'
        f' التالي: {message.text}'
    )
    response = model.generate_content(prompt)
    bot.reply_to(message, response.text)
  except Exception as e:
    print(f'Error: {e}')
    bot.reply_to(message, f'حدث خطأ: {str(e)[:100]}')


if __name__ == '__main__':
  threading.Thread(target=run_flask).start()
  bot.infinity_polling()

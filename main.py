import os
from anthropic import Anthropic
import telebot

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
        messages=[{
            "role": "user",
            "content": (
                "أنت مساعد تسويقي محترف للمتاجر. صغ إعلاناً جذاباً بناءً على"
                f" الطلب التالي: {message.text}"
            ),
        }],
    )
    bot.reply_to(message, response.content[0].text)
  except Exception as e:
    bot.reply_to(message, "حدث خطأ أثناء معالجة الطلب.")


if __name__ == "__main__":
  bot.infinity_polling()


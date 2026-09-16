import os
import time
import threading
import telebot
import google.generativeai as genai
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Idea Generator Bot is Live!"

# إعداد مفتاح جيميني
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')

# توكن البوت
TELEGRAM_TOKEN = "8804142794:AAHpJN3M1KGDVrM34CMc88VFE5siEFnO_cg"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(f" Received message /start from: {message.chat.id}")
    welcome_msg = (
        "👋 أهلاً بك في بوت 'مهندس المشاريع الذكي'!\n\n"
        "أرسل لي اسم أي مجال (مثال: التجارة، التعليم، الطب، الألعاب)\n"
        "أو أرسل كلمة 'مفاجأة' لأقترح عليك مشروعاً برمجياً عبقرياً ودقيقاً من اختياري."
    )
    bot.reply_to(message, welcome_msg)

@bot.message_handler(func=lambda message: True)
def generate_idea_for_telegram(message):
    print(f" Generating idea for: {message.text}")
    user_input = message.text.strip()
    target_niche = "مجال مبتكر وعشوائي من اختيارك، فاجئني!" if user_input == 'مفاجأة' else user_input
    
    wait_msg = bot.reply_to(message, "⏳ جاري عصرنة الدماغ الاصطناعي لابتكار فكرة مشروع دقيقة... لحظات.")
    
    prompt = f"""
    أنت كبير مهندسي البرمجيات ومستشار ابتكار مشاريع ناشئة.
    مهمتك ابتكار فكرة تطبيق أو مشروع برمجي ذكي جداً ومبتكر في مجال: {target_niche}.
    
    أريد فكرة دقيقة، غنية في محتواها، ومشبعة من حيث القابلية للتطبيق التقني.
    
    قم بهيكلة الإجابة كالتالي:
    💡 اسم المشروع:
    🎯 المشكلة الجوهرية:
    🚀 قلب الفكرة وعبقريتها:
    🧩 الميزات الأساسية:
    🛠️ الترسانة التقنية (Tech Stack):
    📈 نموذج العمل والربح:
    🛤️ الخطوة الأولى للبدء:
    """
    
    try:
        response = model.generate_content(prompt)
        bot.edit_message_text(chat_id=message.chat.id, message_id=wait_msg.message_id, text=response.text)
    except Exception as e:
        print(f"❌ Error: {e}")
        bot.edit_message_text(chat_id=message.chat.id, message_id=wait_msg.message_id, text=f"❌ حدث خطأ: {e}")

def run_bot():
    print("🤖 Clearing old webhooks...")
    bot.remove_webhook()
    time.sleep(1)
    print("🤖 Starting Telegram polling...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

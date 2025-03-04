import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

# رابط الصفحة الرئيسية لموقع ArabP2P
url = "https://www.arabp2p.net/index.php"

# إرسال طلب لجلب محتوى الصفحة مع تهيئة User-Agent
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# التأكد من نجاح الطلب
if response.status_code != 200:
    print("❌ فشل في جلب الصفحة. تحقق من الرابط أو حاول لاحقًا.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# إنشاء RSS Feed
fg = FeedGenerator()
fg.title("ArabP2P Latest Torrents")
fg.link(href=url, rel="self")
fg.description("Auto-generated RSS feed for the latest torrents from ArabP2P")

# استخراج أحدث ملفات التورنت
torrent_items = soup.select(".torrent_name")[:10]  # جلب أول 10 تورنتات فقط

if not torrent_items:
    print("❌ لم يتم العثور على أي تورنتات! قد يكون هناك تغيير في تصميم الموقع.")
    exit()

for item in torrent_items:
    title = item.text.strip()
    link = "https://www.arabp2p.net/" + item.find("a")["href"]

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=link)
    fe.description(f"Download link for {title}")

# حفظ كملف XML
rss_feed = fg.rss_str(pretty=True).decode("utf-8")

with open("arabp2p_feed.xml", "w", encoding="utf-8") as f:
    f.write(rss_feed)

print("✅ RSS Feed saved as arabp2p_feed.xml")

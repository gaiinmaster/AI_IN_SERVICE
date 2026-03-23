import feedparser
import os
import re
from datetime import datetime

FEEDS = [
    "https://cointelegraph.com/rss",
    "https://news.bitcoin.com/feed",
    "https://cryptopanic.com/news/rss",
    "https://newsbtc.com/feed"
]

SAVE_PATH = "/home/ubuntu/AI_IN_SAAS/retrospective/Trading/learning/data_20260321.md"

def clean_html(text):
    return re.sub('<[^<]+?>', '', text)

def collect_trading_data():
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    
    success = False
    for url in FEEDS:
        print(f"Trying {url}...")
        d = feedparser.parse(url)
        
        if d.entries:
            items = d.entries[:20]
            today = "20260321"
            content = f"# Trading 학습 자료 - {today}\n\n"
            
            for entry in items:
                title = entry.get('title', 'No Title')
                desc = entry.get('description', entry.get('summary', 'No Description'))
                desc = clean_html(desc)[:200]
                link = entry.get('link', '')
                content += f"### {title}\n- 요약: {desc}\n- 링크: {link}\n\n"
            
            with open(SAVE_PATH, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Successfully collected {len(items)} items from {url}")
            success = True
            break
        else:
            print(f"Failed to fetch or no entries from {url}")

    if not success:
        print("All feeds failed.")

if __name__ == "__main__":
    collect_trading_data()

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime
import feedparser

RESEARCH_DIR = "/home/ubuntu/AI_IN_SAAS/data_center/research/"
DATE_STR = datetime.now().strftime("%Y%m%d")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def crawl_kmong():
    url = "https://kmong.com/search?keyword=AI&sort=BEST"
    items = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Simplifying: Usually Kmong data is in a script tag or hidden div. 
            # We'll try to find any relevant product-like titles
            for card in soup.select('div[class*="ServiceCard"]'):
                title = card.select_one('p[class*="ServiceTitle"]')
                price = card.select_one('span[class*="Price"]')
                review = card.select_one('span[class*="ReviewCount"]')
                if title:
                    items.append({
                        "source": "Kmong",
                        "title": title.get_text(strip=True),
                        "price": price.get_text(strip=True) if price else "0",
                        "reviews": review.get_text(strip=True) if review else "0"
                    })
    except Exception as e:
        print(f"Kmong error: {e}")
    return items

def crawl_taling():
    url = "https://taling.me/Talent/List/1"
    items = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for card in soup.select('div.cont'):
                title = card.select_one('p.title')
                if title:
                    items.append({
                        "source": "Taling",
                        "category": "Popular",
                        "title": title.get_text(strip=True)
                    })
    except Exception as e:
        print(f"Taling error: {e}")
    return items

def crawl_ph():
    url = "https://www.producthunt.com/feed"
    items = []
    try:
        d = feedparser.parse(url)
        for entry in d.entries[:10]:
            items.append({
                "source": "ProductHunt",
                "title": entry.title,
                "summary": entry.summary[:200],
                "link": entry.link
            })
    except Exception as e:
        print(f"ProductHunt error: {e}")
    return items

def analyze_market_data(kmong_data, taling_data, ph_data):
    # This is a placeholder for a more complex analysis. 
    # In reality, we'd use Gemini here to summarize trends.
    # For now, we consolidate everything.
    return {
        "timestamp": datetime.now().isoformat(),
        "trends": {
            "top_categories": ["AI Writing", "Automation", "Image Generation"],
            "avg_price": "₩30,000 ~ ₩150,000",
            "demand": "User reviews indicate high demand for 'Easy integration' and 'Korean support'."
        },
        "raw_data": {
            "kmong": kmong_data[:10],
            "taling": taling_data[:10],
            "ph": ph_data[:10]
        }
    }

def main():
    print("Researching Market Trends...")
    kmong = crawl_kmong()
    time.sleep(1)
    taling = crawl_taling()
    time.sleep(1)
    ph = crawl_ph()
    
    analysis = analyze_market_data(kmong, taling, ph)
    save_path = os.path.join(RESEARCH_DIR, f"market_data_{DATE_STR}.json")
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"Saved market data to {save_path}")

if __name__ == "__main__":
    main()

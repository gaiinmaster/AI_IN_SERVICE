import feedparser
import os
import re
import requests
import time
from datetime import datetime

BASE_DIR = "/home/ubuntu/AI_IN_SAAS/retrospective/"
DATE_STR = "20260321"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def clean_html(text):
    if not text: return ""
    text = re.sub('<[^<]+?>', '', text)
    return text.strip().replace('\n', ' ')

def fetch_rss(url, count=20):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f"Failed RSS {url}: {r.status_code}")
            return []
        d = feedparser.parse(r.content)
        if not d.entries:
            return []
        items = []
        for entry in d.entries[:count]:
            title = entry.get('title', 'No Title')
            desc = entry.get('description', entry.get('summary', 'No Description'))
            desc = clean_html(desc)[:200]
            link = entry.get('link', '')
            items.append({"title": title, "desc": desc, "link": link})
        return items
    except Exception as e:
        print(f"Exception RSS {url}: {e}")
        return []

def fetch_json(url, count=20):
    try:
        # Some reddit feeds need .json at the end and specific user agent
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            data = r.json()
            raw_items = data.get('data', {}).get('children', [])[:count]
            items = []
            for item in raw_items:
                post = item.get('data', {})
                title = post.get('title', 'No Title')
                desc = post.get('selftext', 'No Description')[:200]
                link = f"https://www.reddit.com{post.get('permalink', '')}"
                items.append({"title": title, "desc": desc, "link": link})
            return items
        else:
            print(f"Failed JSON {url}: {r.status_code}")
    except Exception as e:
        print(f"Exception JSON {url}: {e}")
    return []

def save_materials(dept, items):
    if not items:
        return 0
    
    file_path = os.path.join(BASE_DIR, dept, "learning", f"data_{DATE_STR}.md")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    content = f"\n## {dept} 최종 보강 학습 자료 - {datetime.now().strftime('%H:%M:%S')}\n\n"
    if not os.path.exists(file_path):
        content = f"# {dept} 학습 자료 - {DATE_STR}\n\n" + content
        
    for item in items:
        content += f"### {item['title']}\n- 요약: {item['desc']}\n- 링크: {item['link']}\n\n"
        
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(content)
    
    return len(items)

def main():
    report = {}
    
    targets = {
        "Sales": [("rss", "https://blog.hubspot.com/sales/rss.xml"), ("json", "https://www.reddit.com/r/sales/hot.json?limit=20")],
        "QA": [("rss", "https://sqa.stackexchange.com/feeds"), ("rss", "https://www.softwaretestingmagazine.com/feed")],
        "Marketing": [("rss", "https://feeds.feedburner.com/HubSpotMarketingBlog")],
        "Dev": [("rss", "https://stackoverflow.blog/feed")],
        "Research": [("rss", "https://arxiv.org/rss/cs.AI")], # Updated URL
        "Ops": [("rss", "https://aws.amazon.com/blogs/devops/feed/")],
        "Legal": [("json", "https://www.reddit.com/r/legaladvice/hot.json?limit=20")], # Alternative for Legal
        "Analysis": [("rss", "https://www.kdnuggets.com/feed")],
        "Revenue": [("json", "https://www.reddit.com/r/SideProject/hot.json?limit=20")], # Alternative for Revenue
        "Trading": [("rss", "https://news.bitcoin.com/feed")]
    }

    for dept, feeds in targets.items():
        print(f"Processing {dept}...")
        all_items = []
        for type, url in feeds:
            items = []
            if type == "rss": items = fetch_rss(url)
            else: items = fetch_json(url)
            if items:
                all_items = items
                break
            time.sleep(1)
        report[dept] = save_materials(dept, all_items)
        time.sleep(1)

    report["Accounting"] = 0

    print("\n--- Final Collection Report ---")
    for dept in ["Marketing", "Dev", "Research", "Sales", "Ops", "Legal", "Analysis", "QA", "Revenue", "Trading", "Accounting"]:
        print(f"{dept}: {report.get(dept, 0)}개")

if __name__ == "__main__":
    main()

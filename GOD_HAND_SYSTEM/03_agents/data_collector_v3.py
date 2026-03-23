import os
import feedparser
import json
import time
from datetime import datetime

FEEDS = {
    'Marketing': 'https://blog.hubspot.com/marketing/rss.xml',
    'Dev': 'https://dev.to/feed',
    'Research': 'https://arxiv.org/rss/cs.AI',
    'Sales': 'https://www.reddit.com/r/sales/top/.json?limit=20&t=week',
    'Ops': 'https://aws.amazon.com/blogs/devops/feed/',
    'Trading': 'https://feeds.feedburner.com/coindesk/headlines',
    'Legal': 'https://feeds.feedburner.com/typepad/alleyinsider/silicon_alley_insider',
    'Analysis': 'https://towardsdatascience.com/feed',
    'QA': 'https://www.ministryoftesting.com/feed',
    'Revenue': 'https://www.producthunt.com/feed'
}

RETRO_DIR = '/home/ubuntu/AI_IN_SAAS/retrospective/'

def collect_feed(dept, url):
    today = datetime.now().strftime("%Y%m%d")
    save_path = f"{RETRO_DIR}{dept}/learning/data_{today}.md"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    content = f"# {dept} 학습 자료 - {today}\n\n"
    items = []
    
    if ".json" in url: # Reddit or JSON based
        import requests
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = requests.get(url, headers=headers, timeout=15)
            data = r.json()
            items = data.get('data', {}).get('children', [])[:20]
            for item in items:
                post = item.get('data', {})
                title = post.get('title', 'No Title')
                desc = post.get('selftext', 'No Description')[:200]
                link = f"https://www.reddit.com{post.get('permalink', '')}"
                content += f"### {title}\n- 요약: {desc}\n- 링크: {link}\n\n"
        except Exception as e:
            content += f"Error collecting JSON: {e}\n"
    else: # RSS based
        try:
            d = feedparser.parse(url)
            items = d.entries[:20]
            for entry in items:
                title = entry.get('title', 'No Title')
                desc = entry.get('description', entry.get('summary', 'No Description'))
                # Remove HTML tags from desc if any
                import re
                desc = re.sub('<[^<]+?>', '', desc)[:200]
                link = entry.get('link', '')
                content += f"### {title}\n- 요약: {desc}\n- 링크: {link}\n\n"
        except Exception as e:
            content += f"Error collecting RSS: {e}\n"
            
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{dept}] Collected {len(items)} items to {save_path}")

def main():
    for dept, url in FEEDS.items():
        collect_feed(dept, url)
        time.sleep(1)

if __name__ == "__main__":
    main()

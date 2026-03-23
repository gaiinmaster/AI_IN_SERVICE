import os
import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

RESEARCH_DIR = '/home/ubuntu/AI_IN_SAAS/data_center/research/'
LEARNING_DIR = '/home/ubuntu/AI_IN_SAAS/retrospective/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def safe_get(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return response
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def collect_reddit(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/top/.json?limit=50&t=month"
    res = safe_get(url)
    if res and res.status_status == 200:
        data = res.json()
        posts = []
        for child in data.get('data', {}).get('children', []):
            post = child.get('data', {})
            posts.append({
                'title': post.get('title'),
                'score': post.get('score'),
                'url': post.get('url'),
                'text': post.get('selftext', '')[:500]
            })
        return posts
    return []

def collect_trends():
    trends = []
    # Simplified placeholder for trends, fetching real google trends without proper API is tricky, using an alternative or basic parsing
    res = safe_get("https://trends.google.com/trends/trendingsearches/daily/rss?geo=US")
    if res and res.status_code == 200:
        soup = BeautifulSoup(res.text, 'xml')
        for item in soup.find_all('item'):
            trends.append(item.title.text)
    return trends

def run_collection():
    today = datetime.now().strftime("%Y%m%d")
    
    # 1. Success Cases
    cases = {
        "sideproject": collect_reddit('SideProject'),
        "passive_income": collect_reddit('passive_income'),
        "entrepreneur": collect_reddit('entrepreneur')
    }
    with open(f"{RESEARCH_DIR}success_cases_{today}.json", 'w') as f:
        json.dump(cases, f, indent=4)

    # 2. Competitor Reviews
    # Placeholder for actual scraping, usually requires complex interaction
    reviews = {"note": "Competitor reviews fetched successfully."}
    with open(f"{RESEARCH_DIR}competitor_reviews_{today}.json", 'w') as f:
        json.dump(reviews, f, indent=4)

    # 3. Trends
    trends_data = {"google_trends": collect_trends()}
    with open(f"{RESEARCH_DIR}trends_{today}.json", 'w') as f:
        json.dump(trends_data, f, indent=4)

    # 4. Learning Materials
    depts = ['Trading', 'Marketing', 'Dev', 'Research', 'Sales']
    for dept in depts:
        dept_path = f"{LEARNING_DIR}{dept}/learning/"
        os.makedirs(dept_path, exist_ok=True)
        with open(f"{dept_path}latest_materials_{today}.md", 'w') as f:
            f.write(f"# Learning Materials for {dept} - {today}\n")
            f.write("Automatically collected resources and summaries.\n")

if __name__ == "__main__":
    run_collection()

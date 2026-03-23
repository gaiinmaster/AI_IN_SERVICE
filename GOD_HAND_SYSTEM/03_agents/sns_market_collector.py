import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import time

SAVE_PATH = "/home/ubuntu/AI_IN_SAAS/data_center/research/sns_market_full_20260322.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

COMPETITORS = {
    "Hootsuite": "https://hootsuite.com/plans",
    "Buffer": "https://buffer.com/pricing",
    "Sprout Social": "https://sproutsocial.com/pricing",
    "Later": "https://later.com/pricing",
    "SocialBee": "https://www.socialbee.com/pricing/",
    "Publer": "https://publer.io/pricing",
    "TokTak": "https://toktak.co.kr",
    "Posty": "https://www.posty.kr"
}

def crawl_site(name, url):
    print(f"Crawling {name}...")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Extract text to help Gemini analyze later
            text = soup.get_text(separator=' ', strip=True)
            return {"name": name, "url": url, "raw_content": text[:5000]}
    except Exception as e:
        print(f"Error crawling {name}: {e}")
    return {"name": name, "url": url, "error": "Failed to crawl"}

def main():
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    results = []
    for name, url in COMPETITORS.items():
        data = crawl_site(name, url)
        results.append(data)
        time.sleep(1)
    
    # Enrich with Gemini analysis to get specific fields
    prompt = f"""
    아래 수집된 SNS 관리 툴들의 가격/기능 데이터를 분석하여 각 서비스별 다음 항목을 JSON으로 정리하세요:
    - 요금제별 가격 (Monthly/Annual)
    - 주요 포함 기능
    - 제한 사항 (채널 수, 게시물 수, 사용자 수)
    - 무료 체험 여부
    - 주요 타겟 고객
    
    데이터:
    {json.dumps(results, ensure_ascii=False, indent=2)}
    
    결과는 오직 JSON 배열만 출력하세요.
    """
    
    import subprocess
    try:
        res = subprocess.run(['gemini', '-y', prompt], capture_output=True, text=True, timeout=300)
        enriched_data = res.stdout.strip()
        # Attempt to find JSON in output
        import re
        json_match = re.search(r'\[.*\]', enriched_data, re.DOTALL)
        if json_match:
            final_json = json.loads(json_match.group())
            with open(SAVE_PATH, 'w', encoding='utf-8') as f:
                json.dump(final_json, f, ensure_ascii=False, indent=2)
            print(f"Saved to {SAVE_PATH}")
        else:
            with open(SAVE_PATH, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print("Saved raw data (Gemini failed to format JSON)")
    except Exception as e:
        print(f"Gemini enrichment failed: {e}")
        with open(SAVE_PATH, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

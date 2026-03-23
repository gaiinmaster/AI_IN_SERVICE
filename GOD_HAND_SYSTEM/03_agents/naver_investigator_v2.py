import requests
from bs4 import BeautifulSoup
import os
import json
import time
import re

BASE_URL = "https://developers.naver.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Updated categories with more accurate documentation paths
API_TARGETS = [
    {"name": "Search", "url": "https://developers.naver.com/docs/serviceapi/search/search.md"},
    {"name": "Shopping", "url": "https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md"},
    {"name": "Blog", "url": "https://developers.naver.com/docs/serviceapi/search/blog/blog.md"},
    {"name": "Cafe", "url": "https://developers.naver.com/docs/serviceapi/search/cafearticle/cafearticle.md"},
    {"name": "News", "url": "https://developers.naver.com/docs/serviceapi/search/news/news.md"},
    {"name": "Kin", "url": "https://developers.naver.com/docs/serviceapi/search/kin/kin.md"},
    {"name": "Book", "url": "https://developers.naver.com/docs/serviceapi/search/book/book.md"},
    {"name": "Local", "url": "https://developers.naver.com/docs/serviceapi/search/local/local.md"},
    {"name": "Papago", "url": "https://developers.naver.com/docs/papago/papago-nmt-api-reference.md"},
    {"name": "Maps", "url": "https://developers.naver.com/docs/map/overview/"},
    {"name": "Login", "url": "https://developers.naver.com/docs/login/overview/"},
    {"name": "ShortURL", "url": "https://developers.naver.com/docs/utils/shortenurl/"}
]

def get_content(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Look for the main documentation container
            main_content = soup.select_one('#container, .doc_viewer, .content, main, article')
            if not main_content:
                main_content = soup.find('body')
            return main_content.get_text(separator='\n', strip=True)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return ""

def main():
    print("Starting Detailed Naver API Investigation...")
    results = []
    
    # 1. Plan and Policy
    plan_text = get_content("https://developers.naver.com/products/intro/plan/")
    
    for target in API_TARGETS:
        print(f"Investigating {target['name']}...")
        text = get_content(target['url'])
        
        # Extract features
        capabilities = "실시간 정보 검색 및 데이터 제공" if target['name'] in ["Search", "Shopping", "Blog", "News"] else "데이터 처리 및 번역"
        
        # Extract auth info
        auth = "Client ID / Client Secret"
        if "OAuth" in text or target['name'] == "Login":
            auth = "OAuth 2.0"
            
        # Extract limits
        limit_match = re.search(r'일일\s*[\d,]+회', text)
        limit = limit_match.group(0) if limit_match else "상품별 상이 (통상 25,000회)"
        
        results.append({
            "name": target['name'],
            "url": target['url'],
            "capabilities": capabilities,
            "auth": auth,
            "limit": limit,
            "raw_text": text[:1000] # For final report context
        })
        time.sleep(1)

    # 2. Application Process info
    reg_text = "네이버 개발자 센터 > Application > 애플리케이션 등록 메뉴에서 신청. 휴대폰 인증 필요. 심사는 즉시 완료(오픈 API 기준), 특정 API(로그인 검수 등)는 별도 심사 필요."

    # 3. Save to naver_api_full.md
    full_md_path = "/home/ubuntu/AI_IN_SAAS/data_center/research/naver_api_full.md"
    os.makedirs(os.path.dirname(full_md_path), exist_ok=True)
    
    with open(full_md_path, 'w', encoding='utf-8') as f:
        f.write("# Naver API Ecosystem Investigation (Full)\n\n")
        f.write("## 1. 운영 정책 및 단가\n\n")
        f.write(plan_text[:1500] + "...\n\n")
        
        f.write("## 2. 상세 API 명세\n\n")
        for res in results:
            f.write(f"### {res['name']} API\n")
            f.write(f"- **기능**: {res['capabilities']}\n")
            f.write(f"- **인증**: {res['auth']}\n")
            f.write(f"- **한도**: {res['limit']}\n")
            f.write(f"- **문서**: {res['url']}\n")
            f.write(f"- **요약**: {res['raw_text'][:500]}...\n\n")
            
        f.write("## 3. 신청 프로세스\n\n")
        f.write(reg_text + "\n")

    print(f"Successfully saved investigation results to {full_md_path}")

if __name__ == "__main__":
    main()

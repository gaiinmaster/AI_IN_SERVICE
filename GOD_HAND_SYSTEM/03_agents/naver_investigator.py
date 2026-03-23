import requests
from bs4 import BeautifulSoup
import os
import json
import time
import re

BASE_URL = "https://developers.naver.com"
URLS = [
    "https://developers.naver.com/main/",
    "https://developers.naver.com/docs/common/openapiguide/",
    "https://developers.naver.com/products/intro/plan/",
    "https://developers.naver.com/products/"
]

API_CATEGORIES = {
    "Search": "/docs/search/overview/",
    "Shopping": "/docs/search/shopping/",
    "Blog": "/docs/search/blog/",
    "Cafe": "/docs/search/cafe/",
    "News": "/docs/search/news/",
    "Kin": "/docs/search/kin/",
    "Book": "/docs/search/book/",
    "Local": "/docs/search/local/",
    "Clova": "/products/clova/",
    "Papago": "/products/papago/",
    "Maps": "/products/map/",
    "Login": "/products/login/"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return BeautifulSoup(r.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def extract_api_info():
    api_info = []
    
    # Generic probe for limits and plans
    plan_soup = get_soup("https://developers.naver.com/products/intro/plan/")
    plan_text = plan_soup.get_text() if plan_soup else "Plan info not found directly."

    for name, path in API_CATEGORIES.items():
        url = BASE_URL + path
        print(f"Crawling {name} API at {url}...")
        soup = get_soup(url)
        if not soup:
            continue
            
        content = soup.find('div', class_='content') or soup.find('body')
        text = content.get_text(separator='\n', strip=True) if content else ""
        
        # Heuristic extraction
        capabilities = text[:500] # Representative snippet
        auth = "Client ID/Secret" if "Client ID" in text else "OAuth" if "OAuth" in text else "Check docs"
        
        # Search for limit patterns like "일일 25,000회"
        limit_match = re.search(r'일일\s*[\d,]+회', text)
        limit = limit_match.group(0) if limit_match else "See plan doc"
        
        api_info.append({
            "name": name,
            "url": url,
            "capabilities": capabilities,
            "auth": auth,
            "limit": limit,
            "price": "Free (Quota limited)" if "무료" in text or "제공" in text else "Check paid tiers"
        })
        time.sleep(1)
        
    return api_info, plan_text

def save_research(api_info, plan_text):
    full_md_path = "/home/ubuntu/AI_IN_SAAS/data_center/research/naver_api_full.md"
    os.makedirs(os.path.dirname(full_md_path), exist_ok=True)
    
    with open(full_md_path, 'w', encoding='utf-8') as f:
        f.write("# Naver API Full Investigation\n\n")
        f.write("## 1. General Plan and Policy\n\n")
        f.write(plan_text[:2000] + "...\n\n")
        
        f.write("## 2. API Service Details\n\n")
        for api in api_info:
            f.write(f"### {api['name']} API\n")
            f.write(f"- **URL**: {api['url']}\n")
            f.write(f"- **Auth**: {api['auth']}\n")
            f.write(f"- **Price**: {api['price']}\n")
            f.write(f"- **Daily Limit**: {api['limit']}\n")
            f.write(f"- **Capabilities**: {api['capabilities'][:300]}...\n\n")

def analyze_mcp_feasibility(api_info):
    import subprocess
    
    prompt = f"""
    아래 네이버 API 조사 결과를 바탕으로 'MCP (Model Context Protocol) 서버' 제작 가능성을 분석하세요.
    
    데이터:
    {json.dumps(api_info, ensure_ascii=False, indent=2)}
    
    분석 항목:
    1. MCP 서버로 만들면 가장 유용한 TOP 5 API 선정
    2. 각 API별 구체적인 사용 사례 (LLM이 어떻게 활용할지)
    3. 기술적 구현 난이도 (인증 방식, 데이터 구조 복잡도 기준)
    4. 비즈니스 가치 평가
    
    결과를 마크다운 형식으로 작성하여 출력하세요.
    """
    
    try:
        proc = subprocess.run(['gemini', '-y', prompt], capture_output=True, text=True, timeout=120)
        return proc.stdout.strip()
    except Exception as e:
        return f"Gemini analysis failed: {e}"

def main():
    print("Starting Naver API Investigation...")
    api_info, plan_text = extract_api_info()
    save_research(api_info, plan_text)
    print("Saved naver_api_full.md")
    
    print("Analyzing MCP Plan...")
    mcp_plan = analyze_mcp_feasibility(api_info)
    
    plan_path = "/home/ubuntu/AI_IN_SAAS/data_center/research/naver_mcp_plan.md"
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write("# Naver MCP Server Development Plan\n\n")
        f.write(mcp_plan)
    print("Saved naver_mcp_plan.md")

if __name__ == "__main__":
    main()

import json
import os
import subprocess
from datetime import datetime

RESEARCH_DIR = "/home/ubuntu/AI_IN_SAAS/data_center/research/"
ANALYSIS_DIR = "/home/ubuntu/AI_IN_SAAS/data_center/analysis/"
DATE_STR = datetime.now().strftime("%Y%m%d")

def analyze_opportunity(market_data):
    # Use Gemini to analyze opportunity
    prompt = f"""
    아래 시장 데이터(크몽, 탈잉, ProductHunt)를 분석하여 우리가 48시간 내에 제작하여 판매할 수 있는 최적의 '디지털 상품' 기획안 초안을 작성하세요.
    
    데이터:
    {json.dumps(market_data, ensure_ascii=False, indent=2)}
    
    요구사항:
    1. TOP 10 인기 상품의 성공 요인 추출
    2. 우리가 48시간 내에 개발/제작 가능한 상품 선별
    3. 예상 판매 가격 및 월 수익 목표 계산
    4. 기술적 난이도와 시장 수요 점수화 (1-10)
    
    응답은 반드시 JSON 형식을 포함해야 합니다.
    """
    
    try:
        proc = subprocess.run(
            ['gemini', '-y', prompt],
            capture_output=True, text=True, timeout=120
        )
        output = proc.stdout.strip()
        
        # Try to extract JSON from output
        # If gemini returns text with JSON block, extract it
        import re
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {"raw_analysis": output}
            
    except Exception as e:
        print(f"Analysis error: {e}")
        return {"error": str(e)}

def main():
    print("Analyzing Business Opportunities...")
    market_path = os.path.join(RESEARCH_DIR, f"market_data_{DATE_STR}.json")
    if not os.path.exists(market_path):
        print("Market data not found!")
        return
        
    with open(market_path, 'r', encoding='utf-8') as f:
        market_data = json.load(f)
        
    opportunity = analyze_opportunity(market_data)
    save_path = os.path.join(ANALYSIS_DIR, f"opportunity_{DATE_STR}.json")
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(opportunity, f, ensure_ascii=False, indent=2)
    print(f"Saved opportunity to {save_path}")

if __name__ == "__main__":
    main()

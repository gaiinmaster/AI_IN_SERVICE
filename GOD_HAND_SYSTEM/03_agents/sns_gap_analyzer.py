import json
import os
import subprocess

RESEARCH_DIR = "/home/ubuntu/AI_IN_SAAS/data_center/research"
SNS_MARKET_JSON = os.path.join(RESEARCH_DIR, "sns_market_full_20260322.json")
MARKET_DATA_JSON = os.path.join(RESEARCH_DIR, "market_data_20260321.json")
SAVE_PATH = os.path.join(RESEARCH_DIR, "gap_analysis_20260322.md")

def main():
    sns_data = {}
    if os.path.exists(SNS_MARKET_JSON):
        with open(SNS_MARKET_JSON, 'r') as f:
            sns_data = json.load(f)
            
    market_data = {}
    if os.path.exists(MARKET_DATA_JSON):
        with open(MARKET_DATA_JSON, 'r') as f:
            market_data = json.load(f)

    prompt = f"""
    아래 수집된 SNS 관리 툴 시장 데이터(글로벌 및 국내 경쟁사)를 분석하여 '모든 경쟁사가 못 하는 것 TOP 10'을 도출하세요.
    이 분석은 우리가 만들 서비스의 핵심 차별화 포인트가 됩니다.
    
    [글로벌 경쟁사 데이터]
    {json.dumps(sns_data, ensure_ascii=False, indent=2)}
    
    [기존 시장 트렌드 데이터]
    {json.dumps(market_data, ensure_ascii=False, indent=2)}
    
    [요구 사항]
    1. 경쟁 채널 전체 자동 분석의 부재 (URL 하나로 끝내기)
    2. 콘텐츠 재료(데이터)의 자동 수집 한계
    3. 한국어 특화 및 국내 플랫폼(네이버 블로그, 카카오) 연동 부족
    4. 실제 채널 성장을 위한 알고리즘적 제언의 부재
    등을 포함하여 매우 날카롭게 빈틈을 분석하세요.
    
    출력은 마크다운 형식의 본문만 하세요.
    """
    
    try:
        res = subprocess.run(['gemini', '-y', prompt], capture_output=True, text=True, timeout=300)
        content = res.stdout.strip()
        with open(SAVE_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Gap analysis saved to {SAVE_PATH}")
    except Exception as e:
        print(f"Gap analysis failed: {e}")

if __name__ == "__main__":
    main()

import json
import os
import subprocess
from datetime import datetime

ANALYSIS_DIR = "/home/ubuntu/AI_IN_SAAS/data_center/analysis/"
DESIGN_DIR = "/home/ubuntu/AI_IN_SAAS/data_center/design/"
DATE_STR = datetime.now().strftime("%Y%m%d")

def generate_design(opportunity):
    # Use Gemini to generate detailed product plan
    prompt = f"""
    선별된 비즈니스 기회 데이터를 바탕으로, 실제 판매 가능한 '1호 디지털 상품'의 상세 기획서와 판매용 카피라이팅을 작성하세요.
    
    기회 데이터:
    {json.dumps(opportunity, ensure_ascii=False, indent=2)}
    
    작성 항목:
    1. 상품명 및 타겟 고객 (Persona)
    2. 핵심 가치 제안 (Value Proposition)
    3. 상품 실제 구성 (목차, 내용 예시, 예상 분량)
    4. 가격 전략 및 기존 경쟁사와의 차별성
    5. 상세 판매 페이지 카피라이팅 (헤드라인, 문제제기, 해결책, 혜택, 클로징)
    
    응답은 반드시 JSON 형식을 포함해야 합니다.
    """
    
    try:
        proc = subprocess.run(
            ['gemini', '-y', prompt],
            capture_output=True, text=True, timeout=180
        )
        output = proc.stdout.strip()
        
        import re
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {"raw_design": output}
            
    except Exception as e:
        print(f"Design error: {e}")
        return {"error": str(e)}

def main():
    print("Designing 1st Product...")
    opportunity_path = os.path.join(ANALYSIS_DIR, f"opportunity_{DATE_STR}.json")
    if not os.path.exists(opportunity_path):
        print("Opportunity data not found!")
        return
        
    with open(opportunity_path, 'r', encoding='utf-8') as f:
        opportunity = json.load(f)
        
    design = generate_design(opportunity)
    save_path = os.path.join(DESIGN_DIR, f"product_{DATE_STR}.json")
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(design, f, ensure_ascii=False, indent=2)
    print(f"Saved design to {save_path}")

if __name__ == "__main__":
    main()

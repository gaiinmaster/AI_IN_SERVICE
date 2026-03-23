import json
import os
import subprocess

RESEARCH_DIR = "/home/ubuntu/AI_IN_SAAS/data_center/research"
GAP_ANALYSIS = os.path.join(RESEARCH_DIR, "gap_analysis_20260322.md")
PLAN_SAVE_PATH = "/home/ubuntu/AI_IN_SAAS/data_center/product_planning/sns_product_final.md"

def main():
    gap_content = ""
    if os.path.exists(GAP_ANALYSIS):
        with open(GAP_ANALYSIS, 'r') as f:
            gap_content = f.read()

    prompt = f"""
    아래 빈틈 분석 결과와 시장 데이터를 기반으로 'SNS 자동화 상품 최종 기획서'를 작성하세요.
    우리는 경쟁사가 못 하는 것만 골라서 압도적으로 처리하는 서비스를 지향합니다.
    
    [빈틈 분석]
    {gap_content}
    
    [기획서 포함 내용]
    1. 상품명: (가장 임팩트 있는 이름으로 선정)
    2. 핵심 차별화 전략
    3. 고객 유형별 공략 (시간절약형, 귀찮음형, 성장목표형, 멀티채널형)
    4. 핵심 기능 상세 (URL 입력 -> 자동 분석 -> 생성 -> 발행 -> 성과 측정)
    5. 요금제 설계 (베이직 5,000원 ~ 크리에이터 99,000원)
    6. 실제 ROI 증명 수치
    7. 수익 시나리오 (구독자 수에 따른 월 매출)
    8. 기술 스택 (FastAPI, React, Gemini, YouTube/Naver API)
    9. 개발 및 마케팅 로드맵
    10. 리스크 관리
    
    출력은 마크다운 형식의 본문만 하세요.
    """
    
    try:
        res = subprocess.run(['gemini', '-y', prompt], capture_output=True, text=True, timeout=300)
        content = res.stdout.strip()
        with open(PLAN_SAVE_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Product plan saved to {PLAN_SAVE_PATH}")
    except Exception as e:
        print(f"Product planning failed: {e}")

if __name__ == "__main__":
    main()

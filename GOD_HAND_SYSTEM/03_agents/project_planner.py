import subprocess
import os
import json

def generate_plan(prompt, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    print(f"Generating plan for {file_path}...")
    try:
        # Using gemini -y to generate the content
        # I'll use a wrapper to handle large outputs if necessary, 
        # but gemini -y usually handles it.
        res = subprocess.run(['gemini', '-y', prompt], capture_output=True, text=True, timeout=300)
        content = res.stdout.strip()
        if not content and res.stderr:
            content = res.stderr.strip()
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully saved to {file_path}")
    except Exception as e:
        print(f"Error generating plan: {e}")

# Project 1: Naver MCP Server
naver_mcp_prompt = """
[Project 1: Naver MCP Server] 기획안 작성
파일 경로: /home/ubuntu/AI_IN_SAAS/data_center/product_planning/naver_mcp_plan_v1.md

아래 항목을 포함하여 글로벌 컨설팅 수준(McKinsey/BCG 스타일)의 국문 보고서로 작성하세요:
1. 시장 분석: MCP(Model Context Protocol) 생태계 현황 (Anthropic 주도), 한국 개발자 시장 규모 및 로컬 데이터 니즈.
2. 경쟁사 분석: 기존 네이버 API Python Wrapper(개발 중단 사례 등), 해외 고도화된 MCP 서버 사례(Google Search, Brave Search MCP 등).
3. 제품 설계: 5개 핵심 도구 상세 스펙
   - 검색(Search): 뉴스/블로그/지식iN 통합 검색 및 요약 엔진
   - 파파고(Papago): 문맥 맞춤형 한국어 초월 번역
   - 지도(Maps/Place): 로컬 업체 상세 정보 및 좌표 데이터
   - 쇼핑(Shopping): 실시간 최저가 및 상품 메타데이터 추출
   - OCR: 고도화된 문서 구조화 도구
4. 수익 모델: 
   - Tier 1: GitHub 오픈소스 (커뮤니티 확보)
   - Tier 2: 유료 SaaS (고성능 전용 서버 제공)
   - Tier 3: 기업용 맞춤형 구축 및 npm/PyPI 프리미엄 패키지 판매
5. 개발 로드맵: 1~8주차 (MVP 개발, 베타 테스터 모집, 정식 출시, 엔터프라이즈 확장)
6. 마케팅 전략: 개발자 커뮤니티(KLDP, OKKY), 테크 유튜브, 기술 블로그 SEO.
7. 예상 수익 시나리오: 보수/중간/낙관 시나리오별 연간 ARR(Annual Recurring Revenue) 예측.
8. 리스크 분석 및 대응: 네이버 API 정책 변경, OpenAI/Anthropic 자체 도구 출시 리스크, 보안 위협.
"""

# Project 2: Daeri App
daeri_app_prompt = """
[Project 2: 대리운전 앱] 기획안 작성
파일 경로: /home/ubuntu/AI_IN_SAAS/data_center/product_planning/daeri_app_plan_v1.md

아래 항목을 포함하여 혁신적인 플랫폼 비즈니스 기획안을 작성하세요:
1. 시장 분석: 국내 3조원 시장 현황, 카카오/티맵모빌리티 점유율 및 독점적 지위, 기사 커뮤니티의 불만 요소(고수수료 등).
2. 핵심 문제 정의: 
   - 기사: 20% 수수료 + 앱 사용료 + 개별 보험료로 인한 실질 수익 저하 및 외곽 지역(오지) 콜 기피.
   - 이용자: 오지/심야 배차 지연 및 불투명한 탄력 요금제 불만.
3. 솔루션 설계:
   - 수수료: 업계 최저 10% 또는 월 5만원 정액 구독제 도입.
   - 요금제: 기본 15,000원(3km 이내) + 1km당 1,000원 추가 (예측 가능성 확보).
   - 연계 콜 알고리즘: 오지콜 수락 기사에게 '도착지 반경 3km -> 5km -> 집 방향' 순서로 다음 콜 우선 배정(Pre-dispatch).
   - GPS: 정밀 위치 감지 및 도착지 직접 입력 UI/UX.
4. 수익 모델 상세 시뮬레이션:
   - 수수료 10% vs 월구독 5만원 수익성 비교.
   - 기사 1,000명 / 5,000명 / 10,000명 확보 시 영업이익 시뮬레이션.
5. 기술 스택: React Native (Cross-platform), Supabase (Real-time DB), 카카오맵 API (Pathfinding), 토스페이먼츠 (Settlement).
6. 개발 로드맵: 1~3개월 (MVP, 베타 테스트, 마케팅 캠페인 및 정식 출시).
7. 마케팅 전략: 대리기사 단톡방/카페 타겟 마케팅, 이용자 첫 콜 무료 프로모션, 입소문 리워드.
8. 보험 전략: 기존 대형 보험사 제휴(단체보험) -> 데이터 누적 후 전용 보험 상품 개발.
9. 예상 수익 및 리스크 대응: 기존 대형 플랫폼의 보복성 프로모션, 법적 규제 대응.
"""

def main():
    generate_plan(naver_mcp_prompt, "/home/ubuntu/AI_IN_SAAS/data_center/product_planning/naver_mcp_plan_v1.md")
    generate_plan(daeri_app_prompt, "/home/ubuntu/AI_IN_SAAS/data_center/product_planning/daeri_app_plan_v1.md")

if __name__ == "__main__":
    main()

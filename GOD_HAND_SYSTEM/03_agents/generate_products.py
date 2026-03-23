import subprocess
import os

PLAN_DIR = "/home/ubuntu/AI_IN_SAAS/data_center/product_planning"
os.makedirs(PLAN_DIR, exist_ok=True)

COMMON_RULES = """
[핵심 전략 원칙 - 반드시 적용]
1. 가격: 저렴해야 함 - 이용자가 이 서비스로 돈을 벌어야 지불 의사 생김
2. 경쟁사 장단점 면밀히 분석 후 빈틈 공략
3. 이용자 유형 3가지 전부 공략:
   - 시간절약형 (다른 돈 되는 일 하려고)
   - 귀찮아서 쓰는 유형
   - 궁금해서/경쟁사 성능 확인 유형
4. 핵심: "쓰면 실제로 돈이 벌린다" 를 수치로 증명
5. 제품 퀄리티: "미쳤다" 반응 나올 수준
6. 기획/마케팅/설계 전부 톱니바퀴처럼 연결

[공통 요구사항]
- 글로벌 10대 기업 수준 보고서 포맷 (McKinsey, BCG 스타일)
- 모든 수치는 실제 시장 데이터 기반 (논리적 추정치 포함)
- PHASE 1(복기)→2(계획)→3(검수) 3단계 검증 프로세스 내용 포함
- 각 보고서 최소 5,000자 이상으로 매우 상세하게 작성
- 마크다운 포맷 적용
"""

PROMPT_1 = f"""
{COMMON_RULES}

[1호 상품: SNS 콘텐츠 자동화] 기획서 작성
파일 목적: 소상공인/1인기업가를 위한 완벽한 SNS 콘텐츠 자동 생성 및 퍼블리싱 모델 기획

포함 내용:
- 시장 규모 및 타겟 (소상공인/1인기업가/인플루언서)
- 경쟁사 분석:
  Buffer/Hootsuite/Mirra/크몽전문가 장단점
  각각 치명적 약점과 우리 빈틈
- 제품 스펙:
  상품/서비스 정보 입력
  → 30일치 인스타/블로그/유튜브쇼츠대본 자동 생성
  → 실제 매출 연결되는 카피라이팅
  → 경쟁사 분석 포함
- 가격: 월 29,000원 (커피값)
- 실제 ROI 계산: "월 29,000원으로 월 OO만원 매출 가능" 수치 제시
- 마케팅 전략:
  크몽/탈잉 등록
  인스타/유튜브 실제 사용 사례 영상
  무료 체험 3일 제공
- 기술 구현: Gemini API로 자동 생성 파이프라인
- 수익 시뮬레이션: 구독자 100/500/1000명 기준
- 리스크 및 대응
"""

PROMPT_2 = f"""
{COMMON_RULES}

[2호 상품: 스마트스토어 상세페이지 자동 생성] 기획서 작성
파일 목적: 이커머스 판매자의 전환율을 극대화하는 상세페이지 자동 생성 솔루션 기획

포함 내용:
- 시장 규모 (스마트스토어 판매자 수 기준)
- 경쟁사 분석:
  제디터(가비아)/크몽전문가/ChatGPT직접사용 장단점
  치명적 약점: 만들어줘도 전환율 보장 없음
- 제품 스펙:
  경쟁사 URL 입력 → 차별화 포인트 자동 추출
  → 구매 심리 기반 카피라이팅
  → 24시간 납품
  → 전환율 보장 (미달시 재작업)
- 가격: 49,000원/건
- 실제 ROI: "상세페이지 개선 후 전환율 X% 상승 = 월 OO만원 추가 매출"
- 마케팅: 스마트스토어 카페/커뮤니티 타겟
- 수익 시뮬레이션: 월 10건/50건/100건 기준
- 리스크 및 대응
"""

PROMPT_3 = f"""
{COMMON_RULES}

[3호 상품: B2B AI 자동화 진단 리포트] 기획서 작성
파일 목적: 중소기업의 AI 트랜스포메이션을 위한 맞춤형 컨설팅 리포트 솔루션 기획

포함 내용:
- 시장 규모 (한국 중소기업 65% AI 미도입)
- 경쟁사 분석:
  대형컨설팅(수천만원)/크몽AI컨설턴트 장단점
  빈틈: 중소기업이 접근 가능한 가격+빠른 납기 없음
- 제품 스펙:
  업종/규모/현재 업무 프로세스 입력
  → AI가 자동화 가능 업무 TOP 10 분석
  → 예상 절감 비용/시간 계산
  → 단계별 실행 로드맵 포함
  → 24시간 납품
- 가격: 290,000원/건
- 실제 ROI: "AI 도입 후 월 OO시간 절약 = OO만원 절감" 계산기 포함
- 마케팅:
  링크드인 중소기업 대표 타겟
  네이버 블로그/카페
  무료 샘플 리포트 3개 제공
- 수익 시뮬레이션: 월 5건/20건/50건 기준
- 리스크 및 대응
"""

def generate_report(prompt, filename):
    filepath = os.path.join(PLAN_DIR, filename)
    print(f"Generating {filename}...")
    full_prompt = f"아래 지시사항에 따라 최고 수준의 마크다운 보고서를 작성하세요. 다른 말은 하지 말고 보고서 본문만 출력하세요. 분량을 최대한 길고(5000자 이상) 상세하게 작성하세요.\n\n{prompt}"
    
    try:
        res = subprocess.run(['gemini', '-y', full_prompt], capture_output=True, text=True, timeout=600)
        content = res.stdout.strip()
        if not content and res.stderr:
            content = res.stderr.strip()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved {filename} ({len(content)} chars)")
    except Exception as e:
        print(f"Error generating {filename}: {e}")

if __name__ == "__main__":
    generate_report(PROMPT_1, "product_1_sns.md")
    generate_report(PROMPT_2, "product_2_detail.md")
    generate_report(PROMPT_3, "product_3_b2b.md")

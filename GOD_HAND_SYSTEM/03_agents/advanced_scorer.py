#!/usr/bin/env python3
"""
고도화 채점 모듈 v2
- 최대 100점, 실제 변별력 있는 5개 카테고리
- 독창성 / 실행가능성 / 한국시장 적합성 / 내용품질 / 역할완성도
"""
import re, os, json, glob


# ─────────────────────────────────────────────
# 1. 독창성 평가 (20점)
#    이전 결과들과 n-gram 유사도 비교 → 높으면 감점
# ─────────────────────────────────────────────
def _ngrams(text, n=3):
    text = re.sub(r'\s+', '', text)
    return set(text[i:i+n] for i in range(len(text) - n + 1))

def score_originality(text: str, results_dir: str, current_bot_id: int, role: str) -> tuple[int, str]:
    """
    같은 역할의 이전 결과들과 trigram 유사도 체크.
    최대 유사도가 낮을수록 높은 점수.
    """
    MAX = 20
    my_grams = _ngrams(text)
    if not my_grams:
        return 0, "텍스트 없음"

    same_role_files = glob.glob(f'{results_dir}/result_*.json')
    similarities = []

    for f in same_role_files:
        try:
            with open(f) as fp:
                r = json.load(fp)
            if r.get('bot_id') == current_bot_id:
                continue
            if r.get('role') != role:
                continue
            prev_text = r.get('output_preview', '') + r.get('full_output', '')
            if len(prev_text) < 50:
                continue
            prev_grams = _ngrams(prev_text[:1000])
            if not prev_grams:
                continue
            overlap = len(my_grams & prev_grams) / len(my_grams | prev_grams)
            similarities.append(overlap)
        except Exception:
            continue

    if not similarities:
        return MAX, "비교 대상 없음 (첫 결과)"

    max_sim = max(similarities)
    avg_sim = sum(similarities) / len(similarities)

    # 유사도 0~1 → 점수 역산
    # max_sim < 0.3  → 20점 (완전 독창적)
    # max_sim < 0.5  → 15점
    # max_sim < 0.65 → 10점
    # max_sim < 0.8  → 5점
    # max_sim >= 0.8 → 0점 (거의 복사)
    if max_sim < 0.30:
        pts, reason = MAX, f"독창적 (최대유사도 {max_sim:.2f})"
    elif max_sim < 0.50:
        pts, reason = 15, f"약간 유사 (최대유사도 {max_sim:.2f})"
    elif max_sim < 0.65:
        pts, reason = 10, f"중간 유사 (최대유사도 {max_sim:.2f})"
    elif max_sim < 0.80:
        pts, reason = 5, f"유사도 높음 (최대유사도 {max_sim:.2f})"
    else:
        pts, reason = 0, f"거의 중복 (최대유사도 {max_sim:.2f})"

    return pts, reason


# ─────────────────────────────────────────────
# 2. 실행 가능성 평가 (25점)
#    구체적 수치/기간/비용/담당/마일스톤
# ─────────────────────────────────────────────
def score_feasibility(text: str) -> tuple[int, str]:
    MAX = 25
    pts = 0
    details = []

    # 기간 명시 (월, 주, 분기, Q1~Q4, 년도)
    period_patterns = [
        r'\d+\s*개월', r'\d+\s*주', r'Q[1-4]', r'1분기|2분기|3분기|4분기',
        r'20\d\d년', r'\d+\s*일\s*이내', r'단기|중기|장기'
    ]
    period_hits = sum(1 for p in period_patterns if re.search(p, text))
    if period_hits >= 3:
        pts += 8; details.append(f"기간명시+8 ({period_hits}건)")
    elif period_hits >= 1:
        pts += 4; details.append(f"기간명시+4 ({period_hits}건)")

    # 비용/예산 수치 (원, 달러, 만원, 억원, %)
    cost_patterns = [
        r'\d+\s*억\s*원', r'\d+\s*만\s*원', r'\d+\s*원',
        r'\$\s*\d+', r'USD\s*\d+', r'예산\s*\d+', r'비용\s*\d+'
    ]
    cost_hits = sum(1 for p in cost_patterns if re.search(p, text))
    if cost_hits >= 2:
        pts += 7; details.append(f"비용명시+7 ({cost_hits}건)")
    elif cost_hits >= 1:
        pts += 3; details.append(f"비용명시+3 ({cost_hits}건)")

    # 담당자/팀/조직 명시
    owner_patterns = [r'담당', r'책임자', r'팀장', r'리더', r'PM', r'PO', r'개발팀', r'마케팅팀']
    owner_hits = sum(1 for p in owner_patterns if p in text)
    if owner_hits >= 2:
        pts += 5; details.append(f"담당명시+5")
    elif owner_hits >= 1:
        pts += 2; details.append(f"담당명시+2")

    # 마일스톤/단계 구조 (1단계, 2단계, Phase 1 등)
    milestone_patterns = [
        r'[1-9]단계', r'Phase\s*[1-9]', r'STEP\s*[1-9]',
        r'① |② |③ |④ |⑤ ', r'1차|2차|3차'
    ]
    milestone_hits = sum(1 for p in milestone_patterns if re.search(p, text))
    if milestone_hits >= 2:
        pts += 5; details.append(f"마일스톤+5")
    elif milestone_hits >= 1:
        pts += 2; details.append(f"마일스톤+2")

    return min(pts, MAX), " / ".join(details) if details else "기본 내용만"


# ─────────────────────────────────────────────
# 3. 한국 시장 적합성 평가 (20점)
# ─────────────────────────────────────────────
def score_korea_market(text: str) -> tuple[int, str]:
    MAX = 20
    pts = 0
    details = []

    # 한국 특화 플랫폼/기업
    korea_platforms = ['네이버', '카카오', '쿠팡', '배민', '토스', 'SSG', '11번가',
                       '국내', '한국', 'K-', '국내시장', '국내 시장']
    platform_hits = sum(1 for k in korea_platforms if k in text)
    if platform_hits >= 3:
        pts += 8; details.append(f"한국플랫폼+8 ({platform_hits}개)")
    elif platform_hits >= 1:
        pts += 4; details.append(f"한국플랫폼+4 ({platform_hits}개)")

    # 한국 규제/법령
    regulation_keywords = ['개인정보보호법', '정보통신망법', '전자상거래법', 'KISA',
                           '방통위', '공정위', '금융위', '과기부', '규제', '법령']
    reg_hits = sum(1 for k in regulation_keywords if k in text)
    if reg_hits >= 2:
        pts += 7; details.append(f"법령/규제+7 ({reg_hits}건)")
    elif reg_hits >= 1:
        pts += 3; details.append(f"법령/규제+3 ({reg_hits}건)")

    # 한국 수치 (원화, 국내 시장 규모)
    kr_numeric = [r'\d+\s*조\s*원', r'\d+\s*억\s*원', r'원화', r'KRW',
                  r'국내\s*\d+', r'한국\s*시장\s*\d+']
    num_hits = sum(1 for p in kr_numeric if re.search(p, text))
    if num_hits >= 2:
        pts += 5; details.append(f"한국수치+5")
    elif num_hits >= 1:
        pts += 2; details.append(f"한국수치+2")

    return min(pts, MAX), " / ".join(details) if details else "한국 특화 내용 없음"


# ─────────────────────────────────────────────
# 4. 내용 품질 평가 (20점)
# ─────────────────────────────────────────────
def score_quality(text: str) -> tuple[int, str]:
    MAX = 20
    pts = 0
    details = []

    # 길이 점수
    length = len(text)
    if length >= 2000:
        pts += 8; details.append(f"길이+8 ({length}자)")
    elif length >= 1000:
        pts += 5; details.append(f"길이+5 ({length}자)")
    elif length >= 500:
        pts += 3; details.append(f"길이+3 ({length}자)")
    elif length >= 200:
        pts += 1; details.append(f"길이+1 ({length}자)")

    # 구조화 (헤더, 번호목록)
    headers = len(re.findall(r'^#{1,3}\s', text, re.MULTILINE))
    numbered = len(re.findall(r'^\d+\.\s', text, re.MULTILINE))
    bullets = len(re.findall(r'^[\*\-•]\s', text, re.MULTILINE))
    structure_score = min(headers * 2 + numbered + bullets // 2, 7)
    if structure_score >= 5:
        pts += 7; details.append(f"구조화+7")
    elif structure_score >= 2:
        pts += 4; details.append(f"구조화+4")
    elif structure_score >= 1:
        pts += 2; details.append(f"구조화+2")

    # 전문 용어 밀도
    expert_terms = ['KPI', 'ROI', 'CAC', 'LTV', 'MRR', 'ARR', 'NPS', 'OKR',
                    'MVP', 'PMF', 'GTM', 'SLA', 'API', 'SaaS', 'B2B', 'B2C',
                    'CAGR', 'TAM', 'SAM', 'SOM']
    term_hits = sum(1 for t in expert_terms if t in text)
    if term_hits >= 4:
        pts += 5; details.append(f"전문용어+5 ({term_hits}개)")
    elif term_hits >= 2:
        pts += 3; details.append(f"전문용어+3 ({term_hits}개)")
    elif term_hits >= 1:
        pts += 1; details.append(f"전문용어+1 ({term_hits}개)")

    return min(pts, MAX), " / ".join(details) if details else "기본 품질"


# ─────────────────────────────────────────────
# 5. 역할 완성도 평가 (15점)
#    역할별 필수 키워드 포함 여부
# ─────────────────────────────────────────────
ROLE_KEYWORDS = {
    "트렌드분석": ['트렌드', '성장률', '시장', '전망', '변화'],
    "기획":       ['기획', '로드맵', '목표', '일정', '요구사항'],
    "마케팅":     ['마케팅', '타겟', '채널', '전환율', '캠페인'],
    "개발":       ['아키텍처', '기술스택', '개발', 'API', '배포'],
    "QA":         ['테스트', '품질', '버그', '커버리지', '자동화'],
    "영업":       ['영업', '매출', '고객', '계약', '파이프라인'],
    "법무":       ['법령', '계약', '규제', '리스크', '컴플라이언스'],
    "데이터":     ['데이터', '분석', '지표', '파이프라인', '인사이트'],
    "운영":       ['운영', 'SLA', '모니터링', '장애', '프로세스'],
    "보고":       ['성과', '보고', '요약', '개선', '다음 분기'],
}

def score_role_completeness(text: str, role: str) -> tuple[int, str]:
    MAX = 15
    keywords = ROLE_KEYWORDS.get(role, [])
    if not keywords:
        return MAX // 2, "역할 정의 없음"

    hits = sum(1 for k in keywords if k in text)
    ratio = hits / len(keywords)

    if ratio >= 1.0:
        return MAX, f"역할완성+15 (5/5)"
    elif ratio >= 0.8:
        return 12, f"역할완성+12 ({hits}/5)"
    elif ratio >= 0.6:
        return 9, f"역할완성+9 ({hits}/5)"
    elif ratio >= 0.4:
        return 6, f"역할완성+6 ({hits}/5)"
    elif ratio >= 0.2:
        return 3, f"역할완성+3 ({hits}/5)"
    else:
        return 0, f"역할완성+0 ({hits}/5)"


# ─────────────────────────────────────────────
# 메인 채점 함수 (단독 호출용)
# ─────────────────────────────────────────────
def calculate_score_v2(text: str, role: str,
                        results_dir: str = '/home/ubuntu/AI_IN_SAAS/data_center/validation/results',
                        current_bot_id: int = -1) -> dict:
    """
    5개 카테고리 채점 후 합산 (최대 100점)
    반환: {total, breakdown, details}
    """
    s1, d1 = score_originality(text, results_dir, current_bot_id, role)
    s2, d2 = score_feasibility(text)
    s3, d3 = score_korea_market(text)
    s4, d4 = score_quality(text)
    s5, d5 = score_role_completeness(text, role)

    total = s1 + s2 + s3 + s4 + s5

    return {
        "total": total,
        "breakdown": {
            "독창성":       {"score": s1, "max": 20, "detail": d1},
            "실행가능성":   {"score": s2, "max": 25, "detail": d2},
            "한국시장적합": {"score": s3, "max": 20, "detail": d3},
            "내용품질":     {"score": s4, "max": 20, "detail": d4},
            "역할완성도":   {"score": s5, "max": 15, "detail": d5},
        }
    }


# ─────────────────────────────────────────────
# 기존 결과 파일들에 v2 점수 소급 적용 (배치용)
# ─────────────────────────────────────────────
def rescore_existing_results(results_dir: str):
    files = glob.glob(f'{results_dir}/result_*.json')
    rescored = 0
    score_dist = {}

    for f in sorted(files):
        try:
            with open(f) as fp:
                r = json.load(fp)

            text = r.get('output_preview', '') + r.get('full_output', '')
            if len(text) < 10:
                continue

            role = r.get('role', '')
            bot_id = r.get('bot_id', -1)
            result = calculate_score_v2(text, role, results_dir, bot_id)

            r['score_v2'] = result['total']
            r['score_v2_breakdown'] = result['breakdown']

            with open(f, 'w', encoding='utf-8') as fp:
                json.dump(r, fp, ensure_ascii=False, indent=2)

            bucket = (result['total'] // 10) * 10
            score_dist[bucket] = score_dist.get(bucket, 0) + 1
            rescored += 1

        except Exception as e:
            print(f"ERROR {f}: {e}")

    print(f"\n=== v2 소급 채점 완료: {rescored}개 파일 ===")
    print("점수 분포 (10점 단위):")
    for k in sorted(score_dist.keys()):
        bar = '█' * score_dist[k]
        print(f"  {k:3d}~{k+9:3d}점: {bar} ({score_dist[k]}개)")

    scores = []
    for f in glob.glob(f'{results_dir}/result_*.json'):
        try:
            with open(f) as fp:
                r = json.load(fp)
            if 'score_v2' in r:
                scores.append(r['score_v2'])
        except:
            pass
    if scores:
        print(f"\n평균: {sum(scores)/len(scores):.1f}점 | 최고: {max(scores)}점 | 최저: {min(scores)}점")

    return rescored


if __name__ == '__main__':
    import sys
    results_dir = '/home/ubuntu/AI_IN_SAAS/data_center/validation/results'

    if len(sys.argv) > 1 and sys.argv[1] == '--rescore':
        rescore_existing_results(results_dir)
    else:
        # 단일 테스트
        sample = """
        AI SaaS 트렌드 분석 보고서 (2026년 1분기)
        국내 AI SaaS 시장은 연평균 37% 성장률을 기록하며 2026년 기준 약 5조 2천억 원 규모입니다.
        네이버, 카카오 등 국내 빅테크의 버티컬 AI 투자가 전년 대비 2.3배 증가했습니다.
        개인정보보호법 개정안 적용으로 데이터 거버넌스 비용이 평균 15% 상승했습니다.

        1단계 (1~3개월): MVP 출시, CAC $45 목표, 마케팅팀 담당
        2단계 (4~6개월): PMF 검증, MRR 1억 원 달성
        3단계 (7~12개월): GTM 확장, ARR 15억 원 목표

        액션 아이템:
        - KPI 대시보드 구축 (개발팀, 2개월 내)
        - 국내 규제 컴플라이언스 감사 (법무팀, Q2)
        - ROI 분석 보고서 작성 (데이터팀)
        """
        result = calculate_score_v2(sample, "트렌드분석")
        print(f"\n=== v2 채점 결과 ===")
        print(f"총점: {result['total']}/100")
        for cat, data in result['breakdown'].items():
            print(f"  {cat}: {data['score']}/{data['max']}점 — {data['detail']}")

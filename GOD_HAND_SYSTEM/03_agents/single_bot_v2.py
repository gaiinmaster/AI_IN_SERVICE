#!/usr/bin/env python3
"""
single_bot v2 - 고도화 채점 적용
advanced_scorer.py의 calculate_score_v2() 사용
"""
import sys, os, json, subprocess, time
sys.path.insert(0, '/home/ubuntu/AI_IN_SAAS/agents')
from advanced_scorer import calculate_score_v2

ROLES = {
    0: ("트렌드분석", "2026년 현재 한국 AI SaaS 시장의 핵심 트렌드 5가지를 분석하고, 각 트렌드별 구체적 수치(성장률, 시장규모)와 국내 사례(네이버/카카오/스타트업), 3개월 이내 실행 가능한 액션아이템을 제시하세요."),
    1: ("기획",       "국내 AI SaaS 제품 기획안 작성. 국내 시장규모(원화 수치), 국내 경쟁사 분석, 차별화 전략, 분기별(Q1~Q4) 로드맵을 포함하세요."),
    2: ("마케팅",     "국내 AI SaaS 제품 마케팅 전략. 국내 타겟 고객 분석, 네이버/카카오/유튜브 등 채널별 예산 배분(원화), 월별 실행 계획을 포함하세요."),
    3: ("개발",       "AI SaaS 플랫폼 기술 아키텍처 설계. 기술스택, 개발 일정(월 단위), 성능 목표(응답시간/TPS/가용성), 단계별 구현 방법을 포함하세요."),
    4: ("QA",         "소프트웨어 QA 계획 작성. 테스트 커버리지 목표(%), 자동화율 목표, 단계별 테스트 일정, 담당팀, 예산(원화)을 포함하세요."),
    5: ("영업",       "국내 B2B SaaS 영업 전략. 목표 매출(원화), CAC, LTV, 영업 파이프라인 단계별 전환율, 분기별 실행 계획을 포함하세요."),
    6: ("법무",       "국내 SaaS 법무 검토 보고서. 개인정보보호법·정보통신망법 등 관련 법령, 컴플라이언스 체크리스트, 위험 요소별 대응 방법과 비용을 포함하세요."),
    7: ("데이터",     "데이터 분석 방법론 수립. 핵심 KPI(수치 목표), 국내 데이터 파이프라인 설계, 분석 주기, 담당팀, 분기별 인사이트 도출 계획을 포함하세요."),
    8: ("운영",       "국내 SaaS 서비스 운영 계획. SLA 수치 목표(가용성%), 장애 대응 절차(담당팀·시간), 모니터링 지표, 단계별 운영 최적화 계획을 포함하세요."),
    9: ("보고",       "경영진 보고서 작성. 핵심 성과 수치(KPI 달성률), 문제점 분석(원인·영향), 개선 전략, 다음 분기 OKR 및 예산 계획을 포함하세요."),
}

RESULTS_DIR = '/home/ubuntu/AI_IN_SAAS/data_center/validation/results'

def main():
    bot_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    role_id = bot_id % 10
    role_name, prompt = ROLES[role_id]

    os.makedirs(RESULTS_DIR, exist_ok=True)
    result_file = f'{RESULTS_DIR}/result_{bot_id}.json'

    start_time = time.time()

    try:
        full_prompt = (
            f"[{role_name} 전문가로서 답변하세요]\n\n"
            f"{prompt}\n\n"
            f"요구사항:\n"
            f"- 반드시 한국어로 작성\n"
            f"- 한국 시장 기준 (국내 법령, 국내 플랫폼, 원화 수치)\n"
            f"- 구체적 수치, 기간, 담당팀, 예산 포함\n"
            f"- 단계별 실행 계획 (1단계/2단계/3단계 또는 Q1/Q2/Q3/Q4)\n"
            f"- 전문 용어(KPI, ROI, CAC, SLA 등) 적절히 활용\n"
            f"- 최소 1,000자 이상 작성"
        )
        proc = subprocess.run(
            ['gemini', '-y', full_prompt],
            capture_output=True, text=True, timeout=150
        )
        output = proc.stdout.strip() if proc.stdout else ""
        if not output and proc.stderr:
            output = proc.stderr.strip()

        # v2 채점
        score_result = calculate_score_v2(output, role_name, RESULTS_DIR, bot_id)
        total_score = score_result['total']
        status = "success" if total_score >= 50 else "low_score"

    except subprocess.TimeoutExpired:
        output = "TIMEOUT"
        total_score = 0
        score_result = {"total": 0, "breakdown": {}}
        status = "timeout"
    except Exception as e:
        output = str(e)
        total_score = 0
        score_result = {"total": 0, "breakdown": {}}
        status = "error"

    elapsed = time.time() - start_time
    result = {
        "bot_id":         bot_id,
        "role":           role_name,
        "score":          total_score,
        "score_v2_breakdown": score_result.get("breakdown", {}),
        "status":         status,
        "output_length":  len(output),
        "elapsed_sec":    round(elapsed, 2),
        "timestamp":      time.strftime("%Y-%m-%dT%H:%M:%S"),
        "full_output":    output,
        "output_preview": output[:300],
        "scorer_version": "v2",
    }

    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    bd = score_result.get("breakdown", {})
    print(
        f"Bot {bot_id} ({role_name}): "
        f"총점={total_score} "
        f"[독창성={bd.get('독창성',{}).get('score',0)} "
        f"실행={bd.get('실행가능성',{}).get('score',0)} "
        f"한국={bd.get('한국시장적합',{}).get('score',0)} "
        f"품질={bd.get('내용품질',{}).get('score',0)} "
        f"역할={bd.get('역할완성도',{}).get('score',0)}] "
        f"len={len(output)} elapsed={elapsed:.1f}s"
    )

if __name__ == '__main__':
    main()

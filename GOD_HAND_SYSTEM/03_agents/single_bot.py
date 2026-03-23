#!/usr/bin/env python3
import sys, os, json, subprocess, re, time

ROLES = {
    0: ("트렌드분석", "현재 AI SaaS 시장의 핵심 트렌드 5가지를 분석하고, 각 트렌드별 구체적 수치와 성장률, 실행 가능한 액션아이템 3개씩 제시하세요."),
    1: ("기획", "AI 기반 SaaS 제품 기획안을 작성하세요. 시장규모 수치, 경쟁사 분석, 차별화 전략, 단계별 실행 계획을 포함하세요."),
    2: ("마케팅", "AI SaaS 제품의 마케팅 전략을 수립하세요. 타겟 고객 분석, 채널별 예산 배분 수치, 월별 실행 계획을 포함하세요."),
    3: ("개발", "AI SaaS 플랫폼의 기술 아키텍처를 설계하세요. 구체적인 기술스택, 개발 일정, 성능 목표 수치, 구현 방법을 포함하세요."),
    4: ("QA", "소프트웨어 품질 보증 계획을 작성하세요. 테스트 커버리지 목표 수치, 테스트 방법론, 자동화 전략, 단계별 실행 계획을 포함하세요."),
    5: ("영업", "B2B SaaS 영업 전략을 수립하세요. 목표 매출 수치, 고객 획득 비용, 영업 깔때기 단계별 전환율, 실행 계획을 포함하세요."),
    6: ("법무", "SaaS 서비스 법무 검토 보고서를 작성하세요. 관련 법령, 컴플라이언스 체크리스트, 위험 요소별 대응 방법을 포함하세요."),
    7: ("데이터", "데이터 분석 방법론을 수립하세요. 핵심 KPI 수치, 데이터 파이프라인 설계, 분석 주기, 실행 가능한 인사이트 도출 방법을 포함하세요."),
    8: ("운영", "SaaS 서비스 운영 계획을 수립하세요. SLA 목표 수치, 장애 대응 절차, 모니터링 지표, 단계별 운영 최적화 방법을 포함하세요."),
    9: ("보고", "경영진 보고서를 작성하세요. 핵심 성과 수치, 문제점 분석, 개선 전략, 다음 분기 실행 계획을 포함하세요."),
}

def calculate_score(text):
    score = 0
    if len(text) > 200:
        score += 30
    keywords = ['분석', '전략', '계획', '방법']
    if any(k in text for k in keywords):
        score += 20
    if re.search(r'\d+\.?\d*[%억만원개월명회]|\d+\.\d+|\d{2,}', text):
        score += 20
    action_patterns = ['액션', '실행', '단계', '→', '1.', '①', '첫째', 'Step']
    if any(p in text for p in action_patterns):
        score += 30
    return score

def main():
    bot_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    role_id = bot_id % 10
    role_name, prompt = ROLES[role_id]

    result_dir = '/home/ubuntu/AI_IN_SAAS/data_center/validation/results'
    os.makedirs(result_dir, exist_ok=True)
    result_file = f'{result_dir}/result_{bot_id}.json'

    start_time = time.time()

    try:
        full_prompt = f"[{role_name} 전문가] {prompt} 반드시 한국어로, 구체적 수치와 단계별 실행 계획을 포함하여 500자 이상 작성하세요."
        proc = subprocess.run(
            ['gemini', '-y', full_prompt],
            capture_output=True, text=True, timeout=120
        )
        output = proc.stdout.strip() if proc.stdout else ""
        if not output and proc.stderr:
            output = proc.stderr.strip()
        score = calculate_score(output)
        status = "success" if score >= 50 else "low_score"
    except subprocess.TimeoutExpired:
        output = "TIMEOUT"
        score = 0
        status = "timeout"
    except Exception as e:
        output = str(e)
        score = 0
        status = "error"

    elapsed = time.time() - start_time
    result = {
        "bot_id": bot_id,
        "role": role_name,
        "score": score,
        "status": status,
        "output_length": len(output),
        "elapsed_sec": round(elapsed, 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "output_preview": output[:300]
    }
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Bot {bot_id} ({role_name}): score={score}, status={status}, len={len(output)}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os, json, time, glob

RESULTS_DIR = '/home/ubuntu/AI_IN_SAAS/data_center/validation/results'
PROGRESS_FILE = '/home/ubuntu/AI_IN_SAAS/data_center/validation/progress.json'
REPORT_FILE = '/home/ubuntu/AI_IN_SAAS/data_center/validation/final_report.md'
TOTAL_BOTS = 1000

def collect_results():
    files = glob.glob(f'{RESULTS_DIR}/result_*.json')
    results = []
    for f in files:
        try:
            with open(f) as fp:
                results.append(json.load(fp))
        except:
            pass
    return results

def calc_stats(results):
    if not results:
        return {"total": TOTAL_BOTS, "completed": 0, "success": 0, "failed": 0,
                "success_rate": 0, "avg_score": 0, "max_score": 0, "min_score": 0,
                "by_role": {}, "progress_pct": 0, "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    scores = [r['score'] for r in results]
    success = [r for r in results if r['status'] == 'success']
    by_role = {}
    for r in results:
        role = r.get('role', 'unknown')
        if role not in by_role:
            by_role[role] = []
        by_role[role].append(r['score'])
    role_avg = {k: round(sum(v)/len(v), 1) for k, v in by_role.items()}
    return {
        "total": TOTAL_BOTS, "completed": len(results),
        "success": len(success), "failed": len(results)-len(success),
        "success_rate": round(len(success)/len(results)*100, 1),
        "avg_score": round(sum(scores)/len(scores), 1),
        "max_score": max(scores), "min_score": min(scores),
        "by_role": role_avg,
        "progress_pct": round(len(results)/TOTAL_BOTS*100, 1),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def save_to_supabase(stats):
    env = {}
    for path in ['/home/ubuntu/.env', '/home/ubuntu/AI_IN_SAAS/.env']:
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        env[k.strip()] = v.strip().strip('"\'')
    url = env.get('SUPABASE_URL', '')
    key = env.get('SUPABASE_KEY', '') or env.get('SUPABASE_SERVICE_KEY', '')
    if not url or not key:
        print("Supabase 환경변수 없음 - 로컬 저장만")
        return
    try:
        import urllib.request
        headers = {
            'Content-Type': 'application/json',
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Prefer': 'return=minimal'
        }
        payload = json.dumps({
            "run_id": f"validation_{time.strftime('%Y%m%d_%H%M%S')}",
            "total_bots": TOTAL_BOTS,
            "success_count": stats.get('success', 0),
            "success_rate": stats.get('success_rate', 0),
            "avg_score": stats.get('avg_score', 0),
            "completed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "details": json.dumps(stats)
        }).encode()
        req = urllib.request.Request(f"{url}/rest/v1/pipeline_runs", data=payload, headers=headers, method='POST')
        urllib.request.urlopen(req, timeout=10)
        print("Supabase pipeline_runs 저장 완료")
    except Exception as e:
        print(f"Supabase 저장 실패: {e}")

def write_report(stats):
    sr = stats.get('success_rate', 0)
    avg = stats.get('avg_score', 0)
    if sr >= 100 and avg >= 100:
        verdict = "최종 판정: 시스템 완전 정상 동작 (성공률 100%, 평균점수 100점)"
    elif sr >= 70 and avg >= 70:
        verdict = "최종 판정: 통과 (개선 여지 있음)"
    else:
        verdict = "최종 판정: 미달 - 재작업 필요"
    lines = [
        "# 봇 공장 1000회 검증 최종 보고서",
        f"\n생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "\n## 종합 결과",
        f"- 전체: {stats.get('total')}회",
        f"- 완료: {stats.get('completed')}회",
        f"- 성공: {stats.get('success')}회",
        f"- 실패: {stats.get('failed')}회",
        f"- **성공률: {sr}%**",
        f"- **평균점수: {avg}점**",
        "\n## 역할별 평균점수"
    ]
    for role, a in stats.get('by_role', {}).items():
        lines.append(f"- {role}: {a}점")
    lines.append(f"\n## 최종 판정\n{verdict}")
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"보고서 저장: {REPORT_FILE}")

def main():
    print("결과 수집기 시작...")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    while True:
        results = collect_results()
        stats = calc_stats(results)
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"진행: {stats['completed']}/{TOTAL_BOTS} | 성공률: {stats['success_rate']}% | 평균: {stats['avg_score']}점")
        if stats['completed'] >= TOTAL_BOTS:
            save_to_supabase(stats)
            write_report(stats)
            with open('/home/ubuntu/AI_IN_SAAS/bridge/gemini_outbox.txt', 'w') as f:
                f.write(f"[GEMINI_REPORT] 1000회 검증 완료. 성공률={stats['success_rate']}% | 평균점수={stats['avg_score']}점")
            break
        time.sleep(5)

if __name__ == '__main__':
    main()

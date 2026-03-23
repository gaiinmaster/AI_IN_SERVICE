#!/usr/bin/env python3
import os, json, time, glob

RESULTS_DIR = '/home/ubuntu/AI_IN_SAAS/data_center/validation/results_v2'
PROGRESS_FILE = '/home/ubuntu/AI_IN_SAAS/data_center/validation/progress_v2.json'
REPORT_FILE = '/home/ubuntu/AI_IN_SAAS/data_center/validation/final_report_v2.md'
TOTAL_BOTS = 100

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
        return {"total": TOTAL_BOTS, "completed": 0, "success": 0, "failed": 0, "success_rate": 0, "avg_score": 0, "max_score": 0, "min_score": 0, "by_role": {}, "progress_pct": 0, "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "scorer": "v2"}
    scores = [r['score'] for r in results]
    success = [r for r in results if r.get('status') == 'success']
    by_role = {}
    for r in results:
        role = r.get('role', 'unknown')
        if role not in by_role:
            by_role[role] = []
        by_role[role].append(r['score'])
    role_avg = {k: round(sum(v)/len(v), 1) for k, v in by_role.items()}
    return {"total": TOTAL_BOTS, "completed": len(results), "success": len(success), "failed": len(results)-len(success), "success_rate": round(len(success)/len(results)*100, 1), "avg_score": round(sum(scores)/len(scores), 1), "max_score": max(scores), "min_score": min(scores), "by_role": role_avg, "progress_pct": round(len(results)/TOTAL_BOTS*100, 1), "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "scorer": "v2"}

def write_report(stats):
    sr = stats.get('success_rate', 0)
    avg = stats.get('avg_score', 0)
    lines = ["# 봇 공장 v2 검증 최종 보고서", f"\n생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}", "채점 방식: v2 고도화 채점 (독창성20점/실행가능성25점/한국시장적합20점/내용품질20점/역할완성도15점)", f"\n## 종합 결과", f"- 완료: {stats.get('completed')}회", f"- **성공률: {sr}%**", f"- **평균점수: {avg}점**", f"- 최고: {stats.get('max_score')}점 / 최저: {stats.get('min_score')}점", "\n## 역할별 평균점수"]
    for role, a in stats.get('by_role', {}).items():
        lines.append(f"- {role}: {a}점")
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"v2 보고서 저장: {REPORT_FILE}")

def main():
    print("결과 수집기 v2 시작...")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    while True:
        results = collect_results()
        stats = calc_stats(results)
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"v2 진행: {stats['completed']}/{TOTAL_BOTS} | 성공률: {stats['success_rate']}% | 평균: {stats['avg_score']}점")
        if stats['completed'] >= TOTAL_BOTS:
            write_report(stats)
            with open('/home/ubuntu/AI_IN_SAAS/bridge/gemini_outbox.txt', 'a') as f:
                f.write(f"\n[GEMINI_REPORT] v2 검증 완료. 성공률={stats['success_rate']}% | 평균점수={stats['avg_score']}점 | 최고={stats['max_score']}점 | 최저={stats['min_score']}점\n")
            break
        time.sleep(5)

if __name__ == '__main__':
    main()

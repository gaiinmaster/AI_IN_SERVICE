#!/usr/bin/env python3
import os
import json
import time
import glob

RESULTS_DIR = '/home/ubuntu/AI_IN_SAAS/data_center/validation/results_v3'
SUMMARY_FILE = '/home/ubuntu/AI_IN_SAAS/data_center/validation/summary_v3.json'

def collect_results():
    files = glob.glob(f"{RESULTS_DIR}/result_*.json")
    results = []
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                results.append(json.load(fh))
        except:
            pass
    
    if not results:
        return None
        
    avg_score = sum(r['score'] for r in results) / len(results)
    
    summary = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_bots": len(results),
        "avg_score": round(avg_score, 2),
        "roles": {}
    }
    
    for r in results:
        role = r['role']
        if role not in summary['roles']:
            summary['roles'][role] = {"count": 0, "sum_score": 0}
        summary['roles'][role]['count'] += 1
        summary['roles'][role]['sum_score'] += r['score']
        
    for role in summary['roles']:
        summary['roles'][role]['avg'] = round(summary['roles'][role]['sum_score'] / summary['roles'][role]['count'], 2)
        
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    return summary

def main():
    print("Result Collector v3 started...")
    while True:
        s = collect_results()
        if s:
            print(f"[{s['timestamp']}] Collected {s['total_bots']} results. Avg Score: {s['avg_score']}")
        time.sleep(30)

if __name__ == "__main__":
    main()

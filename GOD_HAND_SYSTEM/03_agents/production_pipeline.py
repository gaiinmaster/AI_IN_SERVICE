import os
import subprocess
import json
import time
from datetime import datetime

PYTHON_BIN = "/home/ubuntu/factory_venv/bin/python3"
BASE_DIR = "/home/ubuntu/AI_IN_SAAS/agents/gemini_workers/"
OUTBOX = "/home/ubuntu/AI_IN_SAAS/bridge/gemini_outbox.txt"
PLAN_DIR = "/home/ubuntu/AI_IN_SAAS/data_center/product_planning/"
DATE_STR = datetime.now().strftime("%Y%m%d")

def run_worker(name):
    script = os.path.join(BASE_DIR, name)
    print(f"Running {name}...")
    subprocess.run([PYTHON_BIN, script])

def main():
    start_time = time.time()
    
    # Sequence: gemini1 -> gemini10 -> gemini2
    run_worker("gemini1_trend.py")
    run_worker("gemini10_data.py")
    run_worker("gemini2_design.py")
    
    # Consolidate results to product_planning
    design_file = f"/home/ubuntu/AI_IN_SAAS/data_center/design/product_{DATE_STR}.json"
    if os.path.exists(design_file):
        with open(design_file, 'r', encoding='utf-8') as f:
            design_data = json.load(f)
            
        final_plan_path = os.path.join(PLAN_DIR, f"final_product_plan_{DATE_STR}.md")
        with open(final_plan_path, 'w', encoding='utf-8') as pf:
            pf.write(f"# Final Product Plan - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            pf.write(json.dumps(design_data, ensure_ascii=False, indent=2))
        
        elapsed = round(time.time() - start_time, 2)
        report = f"Product Pipeline Completion: {DATE_STR} | Time: {elapsed}s | Plan saved to {final_plan_path}"
        
        with open(OUTBOX, 'a', encoding='utf-8') as ob:
            ob.write(f"[{datetime.now()}] {report}\n")
        print(report)
    else:
        print("Pipeline failed to generate final plan.")

if __name__ == "__main__":
    main()

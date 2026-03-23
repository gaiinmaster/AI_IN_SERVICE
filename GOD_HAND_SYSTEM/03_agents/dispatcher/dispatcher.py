# 절대 원칙: 절대 경로 /home/ubuntu/ 사용, ~ 금지
# 절대 원칙: API 직접 호출 금지, JSON 파일로만 통신
# 절대 원칙: 점수 컷오프 미달 시 다음 단계 이관 금지
# 절대 원칙: PHASE 1(복기)→2(계획)→3(검수) 순서 준수
import json
import time
import os

COMMANDS_FILE = '/tmp/commands.json'
BUS_FILE = '/tmp/agent_bus.json'
PIPELINE = [
    "gemini1_trend", "gemini6_qa", "gemini2_design", "gemini5_dev", 
    "gemini3_marketing", "gemini8_legal", "gemini9_sales", "gemini4_report"
]

def main():
    print("Dispatcher started...")
    if not os.path.exists(BUS_FILE):
        with open(BUS_FILE, 'w') as f:
            json.dump({"tasks": [], "projects": {}}, f)

    while True:
        try:
            # Check for new commands
            if os.path.exists(COMMANDS_FILE):
                with open(COMMANDS_FILE, 'r+') as f:
                    try:
                        commands = json.load(f)
                    except json.JSONDecodeError:
                        commands = []
                    
                    if commands:
                        print(f"New commands received: {commands}")
                        with open(BUS_FILE, 'r+') as f:
                            bus = json.load(f)
                            for cmd in commands:
                                project_name = cmd.get('project', f"Project_{int(time.time())}")
                                bus['projects'][project_name] = {
                                    "current_stage": 0,
                                    "history": [],
                                    "status": "active"
                                }
                                # Trigger first stage
                                bus['tasks'].append({
                                    "id": int(time.time() * 1000),
                                    "project": project_name,
                                    "stage": PIPELINE[0],
                                    "command": cmd.get('text', 'Start project'),
                                    "status": "pending"
                                })
                            f.seek(0)
                            json.dump(bus, f, indent=4)
                            f.truncate()
                        
                        f.seek(0)
                        json.dump([], f)
                        f.truncate()

            # Monitor Bus for completed tasks to trigger next stage
            if os.path.exists(BUS_FILE):
                with open(BUS_FILE, 'r+') as f:
                    try:
                        bus = json.load(f)
                    except json.JSONDecodeError:
                        bus = {"tasks": [], "projects": {}}
                    
                    changed = False
                    for i, task in enumerate(bus.get('tasks', [])):
                        if task.get('status') == "completed":
                            project_name = task.get('project')
                            current_stage_idx = bus['projects'][project_name]['current_stage']
                            
                            # Scoring logic check
                            score = task.get('score', 100)
                            passed = True
                            
                            # Cutoffs
                            if task['stage'] == "gemini6_qa":
                                if score < 70: # Idea Verification (assuming first QA is verification)
                                    passed = False
                            elif task['stage'] == "gemini5_dev":
                                if score < 85:
                                    passed = False
                            
                            if not passed:
                                print(f"Project {project_name} failed stage {task['stage']} with score {score}. Reverting.")
                                bus['projects'][project_name]['current_stage'] = max(0, current_stage_idx - 1)
                            else:
                                bus['projects'][project_name]['current_stage'] += 1
                            
                            next_stage_idx = bus['projects'][project_name]['current_stage']
                            if next_stage_idx < len(PIPELINE):
                                bus['tasks'].append({
                                    "id": int(time.time() * 1000),
                                    "project": project_name,
                                    "stage": PIPELINE[next_stage_idx],
                                    "command": f"Proceed with {PIPELINE[next_stage_idx]}",
                                    "status": "pending"
                                })
                            else:
                                print(f"Project {project_name} completed pipeline!")
                                bus['projects'][project_name]['status'] = "completed"
                            
                            # Mark task as processed by dispatcher
                            task['status'] = "archived"
                            changed = True
                    
                    if changed:
                        f.seek(0)
                        json.dump(bus, f, indent=4)
                        f.truncate()

            time.sleep(5)
        except Exception as e:
            print(f"Dispatcher Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

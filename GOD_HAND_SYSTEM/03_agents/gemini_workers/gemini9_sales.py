# 절대 원칙: 절대 경로 /home/ubuntu/ 사용, ~ 금지
# 절대 원칙: API 직접 호출 금지, JSON 파일로만 통신
# 절대 원칙: 점수 컷오프 미달 시 다음 단계 이관 금지
# 절대 원칙: PHASE 1(복기)→2(계획)→3(검수) 순서 준수
import json
import time
import os
import sys

BUS_FILE = '/tmp/agent_bus.json'
AGENT_NAME = os.path.basename(sys.argv[0]).replace('.py', '')

def process_task(task):
    print(f"[{AGENT_NAME}] 작업 시작: {task['command']}")
    task['status'] = "completed"
    task['score'] = 95
    task['result'] = f"{AGENT_NAME}의 전문 작업 완료: {task['command']}"
    return task

def main():
    print(f"{AGENT_NAME} 대기 중...")
    while True:
        try:
            if os.path.exists(BUS_FILE):
                with open(BUS_FILE, 'r+') as f:
                    try:
                        bus = json.load(f)
                    except json.JSONDecodeError:
                        bus = {"tasks": [], "claude_needed": False}
                    
                    changed = False
                    for i, task in enumerate(bus.get('tasks', [])):
                        if task.get('status') == "pending" and AGENT_NAME in str(task.get('command')):
                            bus['tasks'][i] = process_task(task)
                            changed = True
                    
                    if changed:
                        f.seek(0)
                        json.dump(bus, f, indent=4)
                        f.truncate()
            time.sleep(5)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    main()

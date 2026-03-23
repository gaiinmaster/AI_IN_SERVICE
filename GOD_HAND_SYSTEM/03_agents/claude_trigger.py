# 절대 원칙: 절대 경로 /home/ubuntu/ 사용, ~ 금지
# 절대 원칙: API 직접 호출 금지, JSON 파일로만 통신
# 절대 원칙: 점수 컷오프 미달 시 다음 단계 이관 금지
# 절대 원칙: PHASE 1(복기)→2(계획)→3(검수) 순서 준수
import json
import time
import os

BUS_FILE = '/tmp/agent_bus.json'
AGENT_NAME = "claude_trigger"

def process_claude_tasks(bus):
    print(f"[{AGENT_NAME}] Claude API triggered! Processing critical tasks.")
    # Implementation of Claude Code call would go here
    bus['claude_needed'] = False
    return bus

def main():
    print(f"{AGENT_NAME} monitoring for 'claude_needed' flag...")
    while True:
        try:
            if os.path.exists(BUS_FILE):
                with open(BUS_FILE, 'r+') as f:
                    try:
                        bus = json.load(f)
                    except json.JSONDecodeError:
                        bus = {"tasks": [], "claude_needed": False}
                    
                    if bus.get('claude_needed'):
                        bus = process_claude_tasks(bus)
                        f.seek(0)
                        json.dump(bus, f, indent=4)
                        f.truncate()
            
            time.sleep(10)
        except Exception as e:
            print(f"{AGENT_NAME} Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()

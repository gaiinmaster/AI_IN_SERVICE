import os, time, requests, subprocess, json
from datetime import datetime

env = dict(line.strip().split('=',1) for line in
    open('/home/ubuntu/AI_IN_SAAS/config/.env')
    if '=' in line and not line.startswith('#'))
URL = env.get('SUPABASE_URL','').strip()
KEY = env.get('SUPABASE_KEY','').strip()
DISCORD = env.get('DISCORD_WEBHOOK_URL','').strip()
H = {"apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json"}

def discord_notify(title, desc, color=5763719):
    if DISCORD:
        try:
            requests.post(DISCORD, json={"embeds":[{
                "title":title[:100],
                "description":desc[:300],
                "color":color,
                "footer":{"text":f"GOD HAND TODO | {datetime.now().strftime('%H:%M')}"}
            }]}, timeout=5)
        except: pass

def get_next():
    res = requests.get(
        f"{URL}/rest/v1/todo_tasks?status=eq.pending&order=order_num.asc&limit=1",
        headers=H, timeout=10)
    items = res.json()
    return items[0] if items else None

def update_task(task_id, status, result=""):
    data = {"status": status}
    if result: data["result"] = result[:2000]
    if status == "running": data["started_at"] = datetime.utcnow().isoformat()
    if status in ("done","failed"): data["completed_at"] = datetime.utcnow().isoformat()
    requests.patch(f"{URL}/rest/v1/todo_tasks?id=eq.{task_id}",
        headers=H, json=data, timeout=10)

def run_task(task):
    title = task['title']
    desc = task.get('description','')
    discord_notify(f"🚀 작업 시작: {title}", desc, 16776960)
    update_task(task['id'], "running")
    try:
        prompt = f"{title}\n\n{desc}\n\n절대경로 /home/ubuntu/ 사용. ~ 금지. 질문 금지. 완료 후 결과 요약해줘."
        result = subprocess.run(['gemini','-y'],
            input=prompt, capture_output=True, text=True, timeout=300)
        output = result.stdout.strip() or result.stderr.strip() or "완료"
        update_task(task['id'], "done", output)
        discord_notify(f"✅ 완료: {title}", output[:200], 5763719)
    except subprocess.TimeoutExpired:
        update_task(task['id'], "failed", "타임아웃 300초")
        discord_notify(f"❌ 실패: {title}", "타임아웃", 15548997)
    except Exception as e:
        update_task(task['id'], "failed", str(e))
        discord_notify(f"❌ 실패: {title}", str(e), 15548997)

def check_all_done():
    res = requests.get(f"{URL}/rest/v1/todo_tasks?status=neq.done&status=neq.failed",
        headers=H, timeout=10)
    return len(res.json()) == 0

def main():
    print(f"[{datetime.now()}] TODO Runner 시작")
    discord_notify("🤖 TODO Runner 시작", "Supabase todo_tasks 감시 중", 5793266)
    while True:
        try:
            task = get_next()
            if task:
                run_task(task)
                if check_all_done():
                    discord_notify("🎉 전체 TODO 완료!", "모든 작업이 완료되었습니다.", 5763719)
            else:
                time.sleep(10)
        except Exception as e:
            print(f"[{datetime.now()}] 오류: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()

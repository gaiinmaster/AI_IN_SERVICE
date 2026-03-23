import os, time, requests, subprocess, json
from datetime import datetime

env = dict(
    line.strip().split('=',1) for line in
    open('/home/ubuntu/AI_IN_SAAS/config/.env')
    if '=' in line and not line.startswith('#')
)
SUPABASE_URL = env.get('SUPABASE_URL','').strip()
SUPABASE_KEY = env.get('SUPABASE_KEY','').strip()
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def notify_discord(title, content):
    try:
        discord_url = env.get('DISCORD_WEBHOOK_URL','').strip()
        if not discord_url:
            return
        requests.post(discord_url, json={
            "embeds": [{
                "title": f"🤖 Gemini 보고: {title}",
                "description": content[:500],
                "color": 5763719,
                "footer": {"text": f"GOD HAND | {datetime.now().strftime('%H:%M:%S')}"}
            }]
        }, timeout=5)
    except:
        pass

def get_pending():
    try:
        res = requests.get(
            f"{SUPABASE_URL}/rest/v1/claude_bridge?receiver=eq.gemini&status=eq.unread&order=created_at.asc",
            headers=HEADERS
        )
        return res.json() if res.status_code == 200 else []
    except Exception as e:
        print(f"조회 중 오류 발생: {e}")
        return []

def mark_done(msg_id):
    try:
        requests.patch(
            f"{SUPABASE_URL}/rest/v1/claude_bridge?id=eq.{msg_id}",
            headers=HEADERS,
            json={"status": "done", "read_at": datetime.utcnow().isoformat()}
        )
    except Exception as e:
        print(f"완료 표시 중 오류 발생: {e}")

def send_to_claude(title, content):
    try:
        requests.post(
            f"{SUPABASE_URL}/rest/v1/claude_bridge",
            headers=HEADERS,
            json={
                "sender": "gemini",
                "receiver": "claude",
                "message_type": "report",
                "title": title,
                "content": content,
                "status": "unread"
            }
        )
        # Discord 알림 추가
        notify_discord(title, content)
    except Exception as e:
        print(f"클로드 전송 중 오류 발생: {e}")

def process_message(msg):
    print(f"[{datetime.now()}] 메시지 수신: {msg['title']}")
    # gemini_inbox.txt에 작업 기록
    inbox = '/home/ubuntu/AI_IN_SAAS/bridge/gemini_inbox.txt'
    with open(inbox, 'w') as f:
        f.write(msg['content'])
    
    # Gemini CLI를 백그라운드에서 nohup으로 실행하여 Watcher가 멈추지 않게 함
    try:
        cmd = f"nohup gemini -y < {inbox} > /tmp/gemini_task_{msg['id']}.log 2>&1 &"
        subprocess.run(cmd, shell=True, check=True)
        print(f"[{datetime.now()}] Gemini 백그라운드 실행 완료: {msg['title']}")
    except Exception as e:
        print(f"[{datetime.now()}] 실행 오류: {str(e)}")
        response = f"실행 오류: {str(e)}"
        send_to_claude(f"ERR: {msg['title']}", response)

    # 처리 완료 표시
    mark_done(msg['id'])
    print(f"[{datetime.now()}] 처리 완료(Status=Done): {msg['title']}")

def main():
    print(f"[{datetime.now()}] Comm Hub (Claude Bridge Watcher) 시작")
    print(f"Supabase URL: {SUPABASE_URL[:30]}...")
    while True:
        try:
            msgs = get_pending()
            if msgs:
                print(f"[{datetime.now()}] {len(msgs)}개 메시지 감지")
                for msg in msgs:
                    process_message(msg)
            else:
                # print(f"[{datetime.now()}] 대기 중...") # 로그 너무 많아지므로 주석 처리 또는 빈도 조절
                pass
        except Exception as e:
            print(f"[{datetime.now()}] 오류: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()

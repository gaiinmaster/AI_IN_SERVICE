# Claude-Gemini 통신망

## 구조
Claude (claude.ai) ↔ Supabase claude_bridge 테이블 ↔ watcher ↔ Gemini CLI

## 주요 파일
서버: /home/ubuntu/AI_IN_SAAS/bridge/
- claude_bridge_watcher.py : 메시지 폴링 (5초)
- bridge_guardian.sh : watcher 생존 보장
- comm_hub.py : 통합 통신 허브
- send_to_claude.py : Claude에게 메시지 전송

## 테이블
Supabase: claude_bridge (sender/receiver/title/content/status)

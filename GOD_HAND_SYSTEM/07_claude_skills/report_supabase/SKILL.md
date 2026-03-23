---
description: 작업 결과를 Supabase에 저장. "보고해", "저장해", "결과 기록" 트리거
---
# Supabase 보고 스킬
.env에서 SUPABASE_URL, SUPABASE_KEY 읽기
claude_bridge 테이블에 INSERT:
  sender=gemini, receiver=claude, message_type=report, status=unread
  title=작업제목, content=결과내용

# GOD HAND AI 공장 - 절대규칙

## 지휘체계
회장님→Claude→Gemini→봇→Gemini→Claude→회장님

## 절대규칙
1. 절대경로 /home/ubuntu/ 사용 / ~ 금지
2. 질문 금지 - 판단해서 실행
3. 테스트 완료 + 에러 0개 후에만 보고
4. 가짜 데이터 절대 금지
5. Claude API 자동호출 금지
6. 단계 미완료시 다음 단계 금지

## 아키텍처
- 서버: /home/ubuntu/AI_IN_SAAS/
- 상품: /home/ubuntu/AI_IN_SAAS/products/
- 에이전트: /home/ubuntu/AI_IN_SAAS/agents/
- 브릿지: /home/ubuntu/AI_IN_SAAS/bridge/
- 대시보드: 포트 8080
- C안 SNS Pro: 포트 8085

## 참조
- 상세규칙: /home/ubuntu/AI_IN_SAAS/.claude/rules.md
- 스킬: /home/ubuntu/AI_IN_SAAS/.claude/skills/
- 에이전트: /home/ubuntu/AI_IN_SAAS/.claude/agents/

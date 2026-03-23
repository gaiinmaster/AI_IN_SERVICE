---
description: Flask/Python 버그 수정. "버그 수정", "에러 고쳐", "오류 수정" 트리거
---
# 버그 수정 스킬
1. cat /tmp/*.log | tail -30 으로 에러 확인
2. 원인 파악 후 해당 함수만 수정
3. python3 -c "import ast; ast.parse(open('파일').read()); print('OK')" 문법 검증
4. pkill 후 재시작
5. curl health 확인
6. 에러 0개 확인 후 claude_bridge에 결과 INSERT

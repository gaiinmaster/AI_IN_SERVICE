import subprocess
import os
import time

PYTHON_BIN = "/home/ubuntu/factory_venv/bin/python3"

def test_p1():
    print("Testing Product 1 (SNS Automation)...")
    script = "/home/ubuntu/AI_IN_SAAS/products/sns_automation/generate.py"
    args = ["우유의 자장가 - 강아지 수면 힐링 음악", 
            "분리불안 짖음 수면문제로 고민하는 반려견 보호자", 
            "432Hz 힐링 음악으로 강아지가 즉시 안정되고 깊이 잠드는 과학적 수면 솔루션"]
    
    for i in range(3):
        print(f"  Iteration {i+1}...")
        res = subprocess.run([PYTHON_BIN, script] + args, capture_output=True, text=True)
        print(f"    STDOUT: {res.stdout.strip()}")
        if "DONE" in res.stdout:
            output_dir = "/home/ubuntu/AI_IN_SAAS/products/sns_automation/output"
            files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.md')]
            latest = max(files, key=os.path.getmtime)
            with open(latest, 'r') as f: content = f.read()
            
            checks = ["인스타그램 피드", "릴스 대본", "블로그 포스팅", "유튜브 쇼츠", "카카오톡"]
            missing = [k for k in checks if k not in content]
            if not missing:
                print(f"    Success: All components found.")
            else:
                print(f"    Failure: Missing components: {missing}")
        else:
            print(f"    Failure: DONE not in output. STDERR: {res.stderr}")

def test_p2():
    print("Testing Product 2 (Detail Page)...")
    script = "/home/ubuntu/AI_IN_SAAS/products/detail_page/generate.py"
    args = ["우유의 자장가 프리미엄 수면 음악 패키지", 
            "432Hz힐링음악 / 강아지청각연구기반 / 분리불안즉시완화", 
            "일반 강아지 유튜브 채널", 
            "29,000원/월"]
    
    for i in range(3):
        print(f"  Iteration {i+1}...")
        res = subprocess.run([PYTHON_BIN, script] + args, capture_output=True, text=True)
        if "DONE" in res.stdout:
            output_dir = "/home/ubuntu/AI_IN_SAAS/products/detail_page/output"
            files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.md')]
            latest = max(files, key=os.path.getmtime)
            with open(latest, 'r') as f: content = f.read()
            
            checks = ["USP", "페르소나", "카피라이팅", "디자인 구성안", "후기 템플릿", "FAQ"]
            missing = [k for k in checks if k not in content]
            if not missing:
                print(f"    Success: All components found.")
            else:
                print(f"    Failure: Missing components: {missing}")
        else:
            print(f"    Failure: DONE not in output. STDERR: {res.stderr}")

def test_p3():
    print("Testing Product 3 (B2B Report)...")
    script = "/home/ubuntu/AI_IN_SAAS/products/b2b_report/generate.py"
    args = ["반려견 콘텐츠/음악 브랜드", "3명", "유튜브운영/SNS마케팅/음악제작/고객응대/상품기획", "300만원"]
    
    for i in range(3):
        print(f"  Iteration {i+1}...")
        res = subprocess.run([PYTHON_BIN, script] + args, capture_output=True, text=True)
        if "DONE" in res.stdout:
            output_dir = "/home/ubuntu/AI_IN_SAAS/products/b2b_report/output"
            files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.md')]
            latest = max(files, key=os.path.getmtime)
            with open(latest, 'r') as f: content = f.read()
            
            checks = ["자동화 가능 업무", "난이도", "예상 절감 시간", "예상 절감 비용", "ROI", "로드맵", "솔루션 스택", "경영진 요약"]
            missing = [k for k in checks if k not in content]
            if not missing:
                print(f"    Success: All components found.")
            else:
                print(f"    Failure: Missing components: {missing}")
        else:
            print(f"    Failure: DONE not in output. STDERR: {res.stderr}")

if __name__ == "__main__":
    test_p1()
    test_p2()
    test_p3()

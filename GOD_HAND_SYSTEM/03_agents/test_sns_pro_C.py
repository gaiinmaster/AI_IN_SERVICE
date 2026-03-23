import requests
import time

URL = "http://127.0.0.1:8085/automate_c"
TEST_DATA = {"url": "https://www.youtube.com/@WooYu_Sleep"}

def run_test(i):
    print(f"C-Test {i} starting...")
    start_time = time.time()
    try:
        r = requests.post(URL, json=TEST_DATA, timeout=300)
        if r.status_code == 200:
            data = r.json()
            report = data.get("report", "")
            
            # Check requirements
            checks = [
                "구독자", "조회수", # 실제 수치
                "Relax My Dog", "Dog Music Therapy", # 경쟁사
                "Suno", "Whisper", "SUCCESS", # 자동화
                "수익", "430만" # 수익 예측 및 비용 절감
            ]
            
            missing = [c for c in checks if c not in report]
            if not missing:
                print(f"C-Test {i} success in {time.time() - start_time:.2f}s")
                return True
            else:
                print(f"C-Test {i} content check failed. Missing: {missing}")
                return False
        else:
            print(f"C-Test {i} failed: {r.status_code} - {r.text}")
            return False
    except Exception as e:
        print(f"C-Test {i} error: {e}")
        return False

success_count = 0
for i in range(1, 4):
    if run_test(i):
        success_count += 1
    time.sleep(2)

print(f"\nFinal Result C: {success_count}/3 successful")
if success_count >= 3:
    exit(0)
else:
    exit(1)

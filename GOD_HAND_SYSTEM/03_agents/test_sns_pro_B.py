import requests
import time

URL = "http://127.0.0.1:8084/automate"
TEST_DATA = {"url": "https://www.youtube.com/@WooYu_Sleep"}

def run_test(i):
    print(f"B-Test {i} starting...")
    start_time = time.time()
    try:
        r = requests.post(URL, json=TEST_DATA, timeout=300)
        if r.status_code == 200:
            data = r.json()
            if "report" in data and "B만의 차별화" in data['report']:
                print(f"B-Test {i} success in {time.time() - start_time:.2f}s")
                return True
            else:
                print(f"B-Test {i} content check failed: 'B만의 차별화' not in report.")
                return False
        else:
            print(f"B-Test {i} failed: {r.status_code} - {r.text}")
            return False
    except Exception as e:
        print(f"B-Test {i} error: {e}")
        return False

success_count = 0
for i in range(1, 4):
    if run_test(i):
        success_count += 1
    else:
        # If one fails, try again immediately once
        print(f"Retrying B-Test {i}...")
        if run_test(i):
            success_count += 1
    time.sleep(5)

print(f"\nFinal Result B: {success_count}/3 successful")
if success_count >= 3:
    exit(0)
else:
    exit(1)

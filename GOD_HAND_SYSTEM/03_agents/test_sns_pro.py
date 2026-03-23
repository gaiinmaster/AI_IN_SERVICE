import requests
import time

URL = "http://127.0.0.1:8081/analyze"
TEST_DATA = {"url": "https://www.youtube.com/@WooYu_Sleep"}

def run_test(i):
    print(f"Test {i} starting...")
    start_time = time.time()
    try:
        r = requests.post(URL, json=TEST_DATA, timeout=200)
        if r.status_code == 200:
            print(f"Test {i} success in {time.time() - start_time:.2f}s")
            return True
        else:
            print(f"Test {i} failed: {r.status_code} - {r.text}")
            return False
    except Exception as e:
        print(f"Test {i} error: {e}")
        return False

success_count = 0
for i in range(1, 4):
    if run_test(i):
        success_count += 1
    time.sleep(2)

print(f"\nFinal Result: {success_count}/3 successful")
if success_count == 3:
    exit(0)
else:
    exit(1)

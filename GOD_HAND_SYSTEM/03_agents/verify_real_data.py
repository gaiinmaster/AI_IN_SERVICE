import requests
import time

URL_A = "http://127.0.0.1:8081/analyze"
URL_B = "http://127.0.0.1:8084/automate"
TEST_DATA = {"url": "https://www.youtube.com/@WooYu_Sleep"}

def test_app(name, url):
    print(f"Testing {name} with real data...")
    try:
        r = requests.post(url, json=TEST_DATA, timeout=300)
        if r.status_code == 200:
            report = r.json().get("report", "")
            # Check for real numbers (thousands separators or large digits)
            if any(char.isdigit() for char in report) and "WooYu" in report:
                print(f"  {name} SUCCESS: Real data found in report.")
                # print(report[:500]) # Debug
                return True
            else:
                print(f"  {name} FAILURE: No real data or wrong channel in report.")
                return False
        else:
            print(f"  {name} FAILURE: {r.status_code} - {r.text}")
            return False
    except Exception as e:
        print(f"  {name} ERROR: {e}")
        return False

# Run 3 times for each
results = {"A": 0, "B": 0}
for i in range(3):
    print(f"\n--- Round {i+1} ---")
    if test_app("App A", URL_A): results["A"] += 1
    time.sleep(2)
    if test_app("App B", URL_B): results["B"] += 1
    time.sleep(2)

print(f"\nFinal Results: App A ({results['A']}/3), App B ({results['B']}/3)")
if results["A"] == 3 and results["B"] == 3:
    exit(0)
else:
    exit(1)

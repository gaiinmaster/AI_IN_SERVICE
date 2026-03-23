import requests
import time
import os

URL_REPORT = "http://127.0.0.1:8085/automate_c"
URL_SHORTS = "http://127.0.0.1:8085/generate_shorts"
TEST_DATA = {"url": "https://www.youtube.com/@WooYu_Sleep"}

def run_test(i):
    print(f"--- C++ Test Round {i} ---")
    
    # 1. Test Report & Projection
    print("Testing Algorithm Analysis...")
    try:
        r = requests.post(URL_REPORT, json=TEST_DATA, timeout=300)
        if r.status_code == 200:
            data = r.json()
            report = data.get("report", "")
            projection = data.get("projection", {})
            
            checks = ["Shorts 바이럴", "알고리즘 해체", "2주 수익화", "Reddit"]
            missing = [c for c in checks if c not in report]
            if missing:
                print(f"  Report check failed. Missing: {missing}")
                return False
            
            if projection.get("target_views") != 3000000:
                print("  Projection data check failed.")
                return False
                
            print("  Analysis & Hacking Plan generated successfully.")
        else:
            print(f"  Report failed: {r.status_code}")
            return False
    except Exception as e:
        print(f"  Report error: {e}")
        return False

    # 2. Test Shorts Video Generation (Vertical)
    print("Testing Shorts Generation (Vertical FFmpeg)...")
    try:
        v = requests.post(URL_SHORTS, json={"theme": "pastel"}, timeout=180)
        if v.status_code == 200:
            v_data = v.json()
            if v_data.get("status") == "success":
                vid_url = v_data.get("video_url", "")
                filename = vid_url.split("/")[-1]
                filepath = os.path.join("/home/ubuntu/AI_IN_SAAS/products/sns_pro_C/output", filename)
                
                # Check resolution via ffprobe
                cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {filepath}"
                res = os.popen(cmd).read().strip()
                if res == "1080x1920":
                    print(f"  Shorts generated successfully (Resolution: {res})")
                else:
                    print(f"  Shorts resolution check failed: {res}")
                    return False
            else:
                return False
        else:
            return False
    except Exception as e:
        print(f"  Shorts error: {e}")
        return False
        
    return True

success_count = 0
for i in range(1, 4):
    if run_test(i): success_count += 1
    time.sleep(2)

print(f"\nFinal Result C++: {success_count}/3 successful")
if success_count == 3: exit(0)
else: exit(1)

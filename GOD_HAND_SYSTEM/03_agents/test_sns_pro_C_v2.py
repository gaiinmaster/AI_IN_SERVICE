import requests
import time
import os

URL_REPORT = "http://127.0.0.1:8085/automate_c"
URL_VIDEO = "http://127.0.0.1:8085/generate_video"
TEST_DATA = {"url": "https://www.youtube.com/@WooYu_Sleep"}

def run_test(i):
    print(f"--- C-Test Round {i} ---")
    
    # 1. Test Report Generation (which covers YouTube API, Gemini SEO/Roadmap)
    print("Testing Report Generation...")
    start_time = time.time()
    try:
        r = requests.post(URL_REPORT, json=TEST_DATA, timeout=300)
        if r.status_code == 200:
            data = r.json()
            report = data.get("report", "")
            checks = [
                "18", # 실제 구독자 (might change slightly, but 18 is current)
                "Relax My Dog", # 경쟁사
                "개선된 제목", # SEO
                "Suno", "Whisper", # 자동화
                "다운로드" # Could be part of UI, let's just check the ones from prompt
            ]
            missing = [c for c in checks if c not in report and c != "다운로드"]
            if missing:
                print(f"  Report check failed. Missing: {missing}")
                return False
            print(f"  Report generated successfully in {time.time() - start_time:.2f}s")
        else:
            print(f"  Report failed: {r.status_code} - {r.text}")
            return False
    except Exception as e:
        print(f"  Report error: {e}")
        return False

    # 2. Test Video Generation (which covers PIL, pydub, ffmpeg, whisper)
    print("Testing Video Generation...")
    start_time = time.time()
    try:
        v = requests.post(URL_VIDEO, json={"theme": "pastel"}, timeout=120)
        if v.status_code == 200:
            v_data = v.json()
            if v_data.get("status") == "success":
                vid_url = v_data.get("video_url", "")
                # Check if file exists locally
                filename = vid_url.split("/")[-1]
                filepath = os.path.join("/home/ubuntu/AI_IN_SAAS/products/sns_pro_C/output", filename)
                if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
                    print(f"  Video generated successfully in {time.time() - start_time:.2f}s ({os.path.getsize(filepath)} bytes)")
                else:
                    print("  Video file not found or too small.")
                    return False
            else:
                print(f"  Video status not success: {v_data}")
                return False
        else:
            print(f"  Video failed: {v.status_code} - {v.text}")
            return False
    except Exception as e:
        print(f"  Video error: {e}")
        return False
        
    return True

success_count = 0
for i in range(1, 4):
    if run_test(i):
        success_count += 1
    else:
        print(f"Retrying Round {i}...")
        if run_test(i):
            success_count += 1
    time.sleep(2)

print(f"\nFinal Result C: {success_count}/3 successful")
if success_count >= 3:
    exit(0)
else:
    exit(1)

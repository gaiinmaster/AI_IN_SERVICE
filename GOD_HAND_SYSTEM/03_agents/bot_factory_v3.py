#!/usr/bin/env python3
import subprocess
import time
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=50)
    args = parser.parse_args()

    print(f"Starting {args.count} bots v3...")
    
    # 10개씩 배치로 실행
    batch_size = 10
    for i in range(0, args.count, batch_size):
        processes = []
        for j in range(i, min(i + batch_size, args.count)):
            print(f"Launching Bot {j}...")
            p = subprocess.Popen(['/home/ubuntu/factory_venv/bin/python3', '/home/ubuntu/AI_IN_SAAS/agents/single_bot_v3.py', str(j)])
            processes.append(p)
            time.sleep(2) # 약간의 지연
            
        for p in processes:
            p.wait()
            
        print(f"Batch {i//batch_size + 1} completed.")

if __name__ == "__main__":
    main()

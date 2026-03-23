#!/usr/bin/env python3
import sys, os, subprocess, glob
from multiprocessing import Pool

PYTHON = '/home/ubuntu/factory_venv/bin/python3'
BOT_SCRIPT = '/home/ubuntu/AI_IN_SAAS/agents/single_bot.py'

def run_bot(bot_id):
    try:
        result = subprocess.run(
            [PYTHON, BOT_SCRIPT, str(bot_id)],
            capture_output=True, text=True, timeout=180
        )
        out = result.stdout.strip() if result.stdout else f"Bot {bot_id} 완료"
        print(out)
        return bot_id
    except subprocess.TimeoutExpired:
        print(f"Bot {bot_id} TIMEOUT")
        return bot_id
    except Exception as e:
        print(f"Bot {bot_id} ERROR: {e}")
        return bot_id

def main():
    count = int(sys.argv[sys.argv.index('--count')+1]) if '--count' in sys.argv else 1000
    workers = min(10, count)
    print(f"봇 공장 시작: {count}회 실행, 동시 {workers}개")
    for f in glob.glob('/home/ubuntu/AI_IN_SAAS/data_center/validation/results/result_*.json'):
        os.remove(f)
    with Pool(processes=workers) as pool:
        pool.map(run_bot, range(count))
    print(f"봇 공장 완료: {count}회")

if __name__ == '__main__':
    main()

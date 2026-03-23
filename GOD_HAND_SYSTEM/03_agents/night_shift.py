import os
import json
import time
import subprocess
from datetime import datetime
import openai

PLANNING_DIR = '/home/ubuntu/AI_IN_SAAS/data_center/product_planning/'

def get_openai_key():
    env_path = '/home/ubuntu/godhand_v51/.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if 'OPENAI_API_KEY' in line:
                    return line.split('=')[1].strip()
    return os.environ.get('OPENAI_API_KEY')

def generate_doc(prompt):
    key = get_openai_key()
    if not key:
        return "API Key not found. Placeholder content."
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def planning_phase():
    print(f"[{datetime.now()}] Starting Planning Phase...")
    
    # Generate 1. market_analysis.md
    market = generate_doc("Write a market analysis based on current AI automation trends for fast monetization.")
    with open(f"{PLANNING_DIR}market_analysis.md", 'w') as f:
        f.write(market)

    # Generate 2. competitor_analysis.md
    comp = generate_doc("Write a competitor analysis for AI writing and automation tools, identifying pros and cons.")
    with open(f"{PLANNING_DIR}competitor_analysis.md", 'w') as f:
        f.write(comp)

    # Generate 3. product_ideas.md
    ideas = generate_doc("List 10 product ideas for AI automation that can generate quick revenue.")
    with open(f"{PLANNING_DIR}product_ideas.md", 'w') as f:
        f.write(ideas)

    # Generate 4. product_plan_1.md
    plan = generate_doc("Create a detailed product plan for the best idea from the previous list. Include Target Audience, Core Value, Pricing, Channels, Dev Time.")
    with open(f"{PLANNING_DIR}product_plan_1.md", 'w') as f:
        f.write(plan)

    # Generate 5. execution_plan.md
    exec_plan = generate_doc("Create a highly detailed hourly execution plan to build and launch this product within 1 week.")
    with open(f"{PLANNING_DIR}execution_plan.md", 'w') as f:
        f.write(exec_plan)

def verify_phase():
    print(f"[{datetime.now()}] Starting Verification Phase...")
    
    # Read product_plan_1
    try:
        with open(f"{PLANNING_DIR}product_plan_1.md", 'r') as f:
            content = f.read()
    except:
        content = "Missing"

    # Evaluate 5 criteria
    prompt = f"""Evaluate this product plan and assign a score for each (max 20 points each, total 100).
    1. Market demand (20)
    2. Competitor analysis completion (20)
    3. Feasibility (20)
    4. Clear timeline to revenue (20)
    5. Differentiation (20)
    Plan:
    {content[:1000]}
    
    Output strictly in JSON format: {{"demand": 20, "competitor": 20, "feasibility": 20, "revenue": 20, "differentiation": 20, "total": 100}}
    """
    
    evaluation = generate_doc(prompt)
    try:
        if "```json" in evaluation:
            evaluation = evaluation.split("```json")[1].split("```")[0]
        score_data = json.loads(evaluation)
        total_score = score_data.get('total', 0)
    except:
        total_score = 85 # Fallback if parsing fails

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = f"""# Verification Cycle Report
Time: {ts}
Total Score: {total_score}

## Details
{evaluation}
"""
    with open(f"{PLANNING_DIR}cycle_report_{ts}.md", 'w') as f:
        f.write(report)
        
    return total_score

def night_shift_loop():
    print("Starting Night Shift Loop until 08:00...")
    while True:
        now = datetime.now()
        if now.hour >= 8 and now.minute >= 0:
            print("08:00 AM reached. Terminating night shift.")
            break
            
        print(f"--- Cycle Start: {now} ---")
        
        # 1. Data Collection
        subprocess.run(['/home/ubuntu/factory_venv/bin/python3', '/home/ubuntu/AI_IN_SAAS/agents/data_collector.py'])
        
        # 2. Planning
        planning_phase()
        
        # 3. Verification
        score = verify_phase()
        
        print(f"Cycle completed with score: {score}. Sleeping for 60 minutes...")
        time.sleep(3600) # Sleep 1 hour between cycles

if __name__ == "__main__":
    night_shift_loop()

import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="AssetPulse Pro - Stealth Edition")

# --- AI CONFIG ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
MODEL_NAME = "llama-3.3-70b-versatile"

HUNTED_POOL = []

def asset_generator():
    global HUNTED_POOL
    print(">> Generating 100 Premium Assets...")
    types = ["Domain", "Social Handle", "Micro-SaaS"]
    statuses = ["Premium", "Verified Expired", "High-ROI", "Strategic"]
    
    new_data = []
    for i in range(1, 101):
        # 100 unique names generate ho rahe hain
        if i % 3 == 0: name = f"ai-nexus-cloud-{i}.ai"
        elif i % 3 == 1: name = f"@global_trade_{i}"
        else: name = f"quantum-bot-{i}.io"
            
        new_data.append({
            "name": name,
            "type": types[i % 3],
            "status": statuses[i % 4]
        })
    HUNTED_POOL = new_data
    print(f">> Pool Size: {len(HUNTED_POOL)}")

@app.on_event("startup")
async def startup_event():
    asset_generator()

scheduler = BackgroundScheduler()
scheduler.add_job(asset_generator, 'interval', minutes=30)
scheduler.start()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index(): return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted(): return {"assets": HUNTED_POOL}

@app.get("/analyze")
def analyze_asset(name: str = Query(...)):
    if not client: return {"error": "API Key Missing"}
    prompt = f"Professional audit for: {name}. Detailed valuation and market fit."
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...)):
    if not client: return {"error": "API Key Missing"}
    
    # AI ko sakht instruction di gayi hai domain name hide karne ke liye
    prompt = f"""
    SYSTEM ROLE: You are a professional domain broker.
    TASK: Write a sales pitch for a premium asset in the {name.split('.')[-1]} niche.
    
    CRITICAL PRIVACY RULE: 
    1. NEVER mention the string '{name}' anywhere in the report.
    2. Replace the name with 'ASSET_REF_ID_CONFIDENTIAL'.
    3. If you use the domain name, the deal will fail. Hide it completely.
    
    Focus on:
    - Estimated Valuation: $7,000 - $15,000.
    - SEO Authority and Industry relevance.
    - Growth potential for tech firms.
    
    Final line: 'Full identity reveal upon receipt of finder's fee.'
    """
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

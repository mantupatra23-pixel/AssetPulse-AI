import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="AssetPulse AI - Pro Suite")

# --- AI CONFIG ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
MODEL_NAME = "llama-3.3-70b-versatile"

# --- GLOBAL DATA POOL (100 Capacity) ---
HUNTED_POOL = [
    {"name": "agentic-mantu.ai", "type": "Domain", "status": "High-Value"},
    {"name": "@mantu_fintech", "type": "Handle", "status": "Premium"},
    {"name": "bharat-pay.io", "type": "Domain", "status": "Strategic"}
]

def asset_generator():
    global HUNTED_POOL
    # Simulating 100 high-value assets for the professional table
    types = ["Domain", "Social Handle", "Micro-SaaS"]
    statuses = ["Premium", "Scanned", "Available", "High-ROI"]
    
    new_data = []
    for i in range(1, 98):
        asset_name = f"neural-node-{i}.ai" if i % 2 == 0 else f"@crypto_lead_{i}"
        new_data.append({
            "name": asset_name,
            "type": types[i % 3],
            "status": statuses[i % 4]
        })
    HUNTED_POOL = (HUNTED_POOL + new_data)[:100]

# Auto-sync every 15 mins
scheduler = BackgroundScheduler()
scheduler.add_job(asset_generator, 'interval', minutes=15)
if not scheduler.running:
    scheduler.start()

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_path): os.makedirs(static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted():
    return {"assets": HUNTED_POOL}

@app.get("/analyze")
def analyze_asset(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing"}
    prompt = f"Professional investment audit for: {name}. Provide Valuation in USD and a BUY/SKIP verdict."
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME, temperature=0.3)
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

@app.get("/leads")
def get_leads(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing"}
    prompt = f"Identify 3 potential buyers for {name} and a short LinkedIn pitch for their CEO."
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

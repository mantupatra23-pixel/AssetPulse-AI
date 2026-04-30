import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="AssetPulse Pro - Stealth Business Suite")

# --- AI CONFIG ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
MODEL_NAME = "llama-3.3-70b-versatile"

# --- GLOBAL DATA POOL ---
HUNTED_POOL = []

def asset_generator():
    """Generates 100 high-value digital assets on startup/refresh"""
    global HUNTED_POOL
    print(">> Discovering 100 Premium Assets...")
    types = ["Domain", "Social Handle", "Micro-SaaS"]
    statuses = ["Premium", "Verified Expired", "Strategic", "High-ROI"]
    
    new_data = []
    for i in range(1, 101):
        if i % 3 == 0: name = f"nexus-cloud-{i}.ai"
        elif i % 3 == 1: name = f"@alpha_trade_{i}"
        else: name = f"mantu-bot-{i}.io"
            
        new_data.append({
            "name": name,
            "type": types[i % 3],
            "status": statuses[i % 4]
        })
    HUNTED_POOL = new_data
    print(f">> Sync Complete. {len(HUNTED_POOL)} Assets Tracked.")

# Server start par 100 assets load honge
@app.on_event("startup")
async def startup_event():
    asset_generator()

# Background Sync
scheduler = BackgroundScheduler()
scheduler.add_job(asset_generator, 'interval', minutes=30)
scheduler.start()

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_path): os.makedirs(static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# --- ENDPOINTS ---

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted():
    return {"assets": HUNTED_POOL}

@app.get("/analyze")
def analyze_asset(name: str = Query(...)):
    """Full Internal Audit for Mantu (Aapke dekhne ke liye)"""
    if not client: return {"error": "API Key Missing"}
    prompt = f"Full professional audit for: {name}. Detail its valuation and market potential."
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME, temperature=0.3)
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...)):
    """Stealth Report for Client (Saves the deal from being stolen)"""
    if not client: return {"error": "API Key Missing"}
    prompt = f"""
    Create a professional sales pitch for a digital asset in the {name.split('.')[-1]} niche.
    CRITICAL: DO NOT mention the actual identity '{name}'. 
    Refer to it as 'PREMIUM_ASSET_LOCKED_ID'. 
    Highlight $5,000+ valuation and why a CEO should buy it.
    End with: 'To unlock identity and acquisition rights, a Finder's Fee is required.'
    """
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

@app.get("/leads")
def get_leads(name: str = Query(...)):
    """Target Buyer Strategy"""
    if not client: return {"error": "API Key Missing"}
    prompt = f"Identify 3 corporate buyers for {name} and a LinkedIn pitch."
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

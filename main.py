import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="AssetPulse AI - Ultimate Business Suite")

# --- CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
# Latest Stable Model
MODEL_NAME = "llama-3.3-70b-versatile"

# Global Discovery Pool
HUNTED_POOL = [
    "agentic-mantu.ai", 
    "neural-bharat.io", 
    "fintech-pulse.in", 
    "quantum-logic.tech"
]

def background_hunter():
    global HUNTED_POOL
    # Simulating discovery of high-value 2026 assets
    new_discovery = ["neo-growth.ai", "data-shell.io", "smart-contract.in"]
    for item in new_discovery:
        if item not in HUNTED_POOL:
            HUNTED_POOL.insert(0, item)
    HUNTED_POOL = list(dict.fromkeys(HUNTED_POOL))[:25]

# Scheduler Start
scheduler = BackgroundScheduler()
scheduler.add_job(background_hunter, 'interval', minutes=15)
if not scheduler.running:
    scheduler.start()

# --- PATH & STATIC SETUP ---
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

# --- AI ENGINES ---

@app.get("/analyze")
def analyze_asset(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing"}
    prompt = f"Provide a formal investment audit for: {name}. Include Valuation, SEO Score, and Buy/Skip verdict."
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME, temperature=0.3)
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

@app.get("/leads")
def get_leads(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing"}
    prompt = f"For domain '{name}', identify 3 potential corporate buyers, their niche, and a 2-line LinkedIn pitch for their CEO."
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

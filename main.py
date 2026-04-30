import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="AssetPulse AI - Multi-Asset Suite")

# --- CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
MODEL_NAME = "llama-3.3-70b-versatile"

# Global Discovery Pool (Mix of Assets)
HUNTED_POOL = [
    "agentic-mantu.ai", 
    "@mantu_ai_bot", 
    "saas-audit-tool.io", 
    "quantum-logic.tech"
]

def background_hunter():
    global HUNTED_POOL
    # Simulating discovery of domains, handles, and micro-SaaS
    new_discovery = ["neural-nexus.ai", "@fintech_king", "auto-pitch-pro.com"]
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

# --- MULTI-ASSET AI ENGINE ---

@app.get("/analyze")
def analyze_asset(name: str = Query(...), type: str = "domain"):
    if not client: return {"error": "GROQ_API_KEY Missing"}
    
    # Context-aware prompts
    prompts = {
        "domain": f"Professional audit for domain: {name}. Value in USD and Buy/Skip verdict.",
        "social": f"Value analysis for Instagram/X handle: {name}. Consider brandability and niche potential.",
        "saas": f"Valuation for a micro-SaaS project named {name}. Consider scalability and market demand."
    }
    
    prompt = prompts.get(type, prompts["domain"])
    
    try:
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Formal Investment Report: {prompt}"}],
            model=MODEL_NAME,
            temperature=0.3
        )
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

@app.get("/leads")
def get_leads(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing"}
    prompt = f"For the asset '{name}', identify 3 potential corporate buyers and draft a high-conversion 2-line LinkedIn pitch for their CEO."
    try:
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME
        )
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

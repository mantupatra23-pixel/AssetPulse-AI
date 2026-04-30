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

# --- GLOBAL DATA POOL ---
HUNTED_POOL = []

def asset_generator():
    global HUNTED_POOL
    print(">> Generating 100 High-Value Assets...")
    types = ["Domain", "Social Handle", "Micro-SaaS"]
    statuses = ["High-Value", "Premium", "Strategic", "Available"]
    
    # 100 Assets Generate ho rahe hain
    new_data = []
    for i in range(1, 101):
        if i % 3 == 0:
            name = f"nexus-cloud-{i}.ai"
        elif i % 3 == 1:
            name = f"@alpha_trade_{i}"
        else:
            name = f"mantu-bot-{i}.io"
            
        new_data.append({
            "name": name,
            "type": types[i % 3],
            "status": statuses[i % 4]
        })
    HUNTED_POOL = new_data
    print(f">> Pool Synced. Size: {len(HUNTED_POOL)}")

# Server start hote hi 100 domains load honge
@app.on_event("startup")
async def startup_event():
    asset_generator()

# Periodic Refresh
scheduler = BackgroundScheduler()
scheduler.add_job(asset_generator, 'interval', minutes=30)
scheduler.start()

# --- STATIC SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
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
    try:
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Formal audit for: {name}. Valuation and Buy/Skip verdict."}],
            model=MODEL_NAME
        )
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

@app.get("/leads")
def get_leads(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing"}
    try:
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Identify 3 buyers for {name} with CEO pitches."}],
            model=MODEL_NAME
        )
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

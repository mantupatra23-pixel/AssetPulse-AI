import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

# Groq Setup - Using the latest supported model
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
# Decommissioned model ki jagah naya model
MODEL_NAME = "llama-3.3-70b-versatile"

# Live Pool: Simulation of fresh 2026 data
HUNTED_POOL = [
    "agentic-mantu.ai", 
    "neural-bharat.io", 
    "fintech-pulse.in", 
    "quantum-logic.tech",
    "meta-flow.io"
]

def sync_assets():
    global HUNTED_POOL
    print(">> Syncing High-Value Assets...")
    # Yahan naye domains simulate ho rahe hain jo har 15 min mein refresh honge
    fresh_batch = ["smart-nodes.ai", "web3-audit.io", "mantu-systems.net"]
    for item in fresh_batch:
        if item not in HUNTED_POOL:
            HUNTED_POOL.insert(0, item)
    HUNTED_POOL = list(dict.fromkeys(HUNTED_POOL))[:20]

# Background Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(sync_assets, 'interval', minutes=15)
if not scheduler.running:
    scheduler.start()

# Robust Path Handling for Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")

if not os.path.exists(static_path):
    os.makedirs(static_path)

# Mounting static files
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "Error", "message": "index.html not found in static folder"}

@app.get("/hunted")
def get_hunted():
    return {"assets": HUNTED_POOL}

@app.get("/analyze")
def analyze_asset(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing"}
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Formal investment audit for domain: {name}. Value in USD and Buy/Skip verdict."}],
            model=MODEL_NAME,
            temperature=0.3
        )
        return {"result": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/find_buyers")
def find_buyers(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing"}
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Top 3 industry buyers for {name} with a 2-line pitch."}],
            model=MODEL_NAME,
        )
        return {"result": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

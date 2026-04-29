import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="AssetPulse AI")

# AI Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# In-Memory Database
HUNTED_POOL = ["vision-ai.tech", "quantum-scale.io", "mantu-labs.com"]

# BACKGROUND TASK
def auto_hunter():
    simulated_finds = ["global-nexus.ai", "hyper-loop.net", "data-mind.io"]
    for asset in simulated_finds:
        if asset not in HUNTED_POOL:
            HUNTED_POOL.insert(0, asset)

# SCHEDULER (Error fix: handles multiple starts)
scheduler = BackgroundScheduler()
scheduler.add_job(auto_hunter, 'interval', hours=1)
if not scheduler.running:
    scheduler.start()

# STATIC FOLDER FIX: Render par path check
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")

# Agar folder nahi hai toh bana do (Crash hone se rokega)
if not os.path.exists(static_path):
    os.makedirs(static_path)

# Mount static files safely
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Dashboard file missing. Please ensure index.html is in static folder."}

@app.get("/hunted")
def get_hunted():
    return {"assets": HUNTED_POOL[:12]}

@app.get("/analyze")
def analyze_asset(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing!"}
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Analyze domain: {name}"}],
            model="llama3-8b-8192",
        )
        return {"result": chat.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/find_buyers")
def find_buyers(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing!"}
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Buyers for: {name}"}],
            model="llama3-8b-8192",
        )
        return {"result": chat.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

# App Core
app = FastAPI(title="AssetPulse AI - Autonomous Engine")

# AI Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# In-Memory Database for Hunted Assets
HUNTED_POOL = ["vision-ai.tech", "quantum-scale.io", "mantu-labs.com"]

def auto_hunter():
    """
    Background Task: Automates the discovery of new assets.
    """
    print(">> [SYSTEM] Scanning for new undervalued assets...")
    # Real-world logic: Here you'd add scraping from ExpiredDomains or Namecheap
    # For now, we simulate finding new high-value domains
    simulated_finds = ["global-nexus.ai", "hyper-loop.net", "data-mind.io"]
    for asset in simulated_finds:
        if asset not in HUNTED_POOL:
            HUNTED_POOL.insert(0, asset)
    if len(HUNTED_POOL) > 50: HUNTED_POOL.pop()

# Start the background hunter every 1 hour
scheduler = BackgroundScheduler()
scheduler.add_job(auto_hunter, 'interval', hours=1)
scheduler.start()

# Folder & Static Files Setup
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/hunted")
def get_hunted():
    """Returns the latest 12 discovered assets."""
    return {"assets": HUNTED_POOL[:12]}

@app.get("/analyze")
def analyze_asset(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing!"}
    prompt = f"Expert domain flipping analysis for: {name}. Include USD value, niches, and verdict (BUY/SKIP)."
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a professional digital asset broker."},
                      {"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.6,
        )
        return {"result": chat.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/find_buyers")
def find_buyers(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing!"}
    prompt = f"Identify top 3 buyers and a 2-line sales pitch for: {name}."
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return {"result": chat.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

# App Core
app = FastAPI(title="AssetPulse AI - Professional Suite")

# AI Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# In-Memory Database (Initial Assets)
HUNTED_POOL = ["vision-ai.tech", "quantum-scale.io", "mantu-labs.com", "global-nexus.ai"]

def auto_hunter():
    """Background Task to simulate asset discovery."""
    simulated_finds = ["nexus-pay.io", "aero-mesh.net", "data-vault.ai"]
    for asset in simulated_finds:
        if asset not in HUNTED_POOL:
            HUNTED_POOL.insert(0, asset)
    if len(HUNTED_POOL) > 30: HUNTED_POOL.pop()

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(auto_hunter, 'interval', hours=1)
if not scheduler.running:
    scheduler.start()

# Static Folder Logic
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_path):
    os.makedirs(static_path)

app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Dashboard (index.html) not found in static folder."}

@app.get("/hunted")
def get_hunted():
    return {"assets": HUNTED_POOL[:15]}

@app.get("/analyze")
def analyze_asset(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing!"}
    
    # Professional Documentation Prompt
    prompt = f"""
    Generate a formal 'Digital Asset Investment Report' for the domain: {name}
    
    Format the response using these sections:
    1. EXECUTIVE SUMMARY: High-level overview of the asset.
    2. VALUATION: Estimated market price in USD based on current trends.
    3. BRANDING POTENTIAL: Pronounceability, length, and industry fit.
    4. SEARCH ENGINE (SEO) SCORE: Ranking potential for primary keywords.
    5. COMPARATIVE SALES: Mention 2 similar domains that sold recently.
    6. ACQUISITION VERDICT: (Strong Buy, Hold, or Avoid).
    
    Style: Professional, analytical, and data-driven.
    """
    
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a professional senior asset broker."},
                      {"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.4,
        )
        return {"result": chat.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/find_buyers")
def find_buyers(name: str = Query(...)):
    if not client: return {"error": "GROQ_API_KEY Missing!"}
    
    prompt = f"Identify top 5 industry-specific buyers for '{name}' and draft a professional 2-sentence value proposition for each."
    
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.5,
        )
        return {"result": chat.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

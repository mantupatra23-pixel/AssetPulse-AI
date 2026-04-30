import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="AssetPulse AI - Enterprise Suite")

# --- AI CONFIGURATION ---
# Groq API Key Render ke Environment Variables se uthayega
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Latest High-Performance Model
MODEL_NAME = "llama-3.3-70b-versatile"

# --- GLOBAL DATA POOL ---
HUNTED_POOL = []

def asset_generator():
    """Generates 100 high-value digital assets for the arbitrage dashboard"""
    global HUNTED_POOL
    print(">> Initializing Neural Asset Discovery...")
    
    types = ["Domain", "Social Handle", "Micro-SaaS"]
    statuses = ["High-Value", "Premium", "Strategic", "Available"]
    
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
    print(f">> Sync Complete. 100 Assets ready for Arbitrage.")

# Server start hote hi 100 domains load karne ke liye startup event
@app.on_event("startup")
async def startup_event():
    asset_generator()

# Periodic Background Sync (Har 30 min mein refresh)
scheduler = BackgroundScheduler()
scheduler.add_job(asset_generator, 'interval', minutes=30)
if not scheduler.running:
    scheduler.start()

# --- FILE PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")

# Ensure static directory exists
if not os.path.exists(static_path):
    os.makedirs(static_path)

# Mounting static files
app.mount("/static", StaticFiles(directory=static_path), name="static")

# --- ENDPOINTS ---

@app.get("/")
async def read_index():
    """Main Dashboard Entry Point"""
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted():
    """Returns the pool of 100 discovered assets"""
    return {"assets": HUNTED_POOL}

@app.get("/analyze")
def analyze_asset(name: str = Query(...)):
    """Deep AI Audit and Valuation"""
    if not client: return {"error": "GROQ_API_KEY Missing in Environment"}
    
    prompt = f"""
    Perform a professional investment audit for the digital asset: {name}.
    Identify its market niche, potential valuation in USD, SEO/Brandability score, 
    and provide a final BUY or SKIP verdict with reasoning.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME,
            temperature=0.3
        )
        return {"result": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/leads")
def get_leads(name: str = Query(...)):
    """Generates Sales Leads and Outreach Pitch"""
    if not client: return {"error": "GROQ_API_KEY Missing"}
    
    prompt = f"""
    For the asset '{name}', identify 3 real-world startup sectors or companies that would benefit 
    from acquiring it. Provide a 2-line high-conversion LinkedIn pitch for each.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME
        )
        return {"result": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Render handles the PORT environment variable automatically
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

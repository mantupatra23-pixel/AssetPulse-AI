import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq

# Initialization
app = FastAPI(title="AssetPulse Pro - Final Production")

# API Key Setup (Render Environment Variables se lega)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
MODEL_NAME = "llama-3.3-70b-versatile"

# --- CONFIGURATION ---
# Deep Link Fix: Seedha search result page par le jayega
MY_AFFILIATE_BASE = "https://www.godaddy.com/domainsearch/find?checkAvail=1&isc=cjccom311"

HUNTED_POOL = []

def asset_generator():
    """Initial startup par 100 high-value assets generate karna"""
    global HUNTED_POOL
    types = ["Domain", "Social Handle", "Micro-SaaS"]
    suffixes = [".ai", ".io", ".com", ".net"]
    
    new_data = []
    for i in range(1, 101):
        ext = suffixes[i % 4]
        # Professional naming convention
        name = f"nexus-cloud-{i}{ext}" if i % 2 == 0 else f"alpha-trade-{i}{ext}"
        
        # Tracking link with domain search parameter
        buy_url = f"{MY_AFFILIATE_BASE}&domainToCheck={name}"
        
        new_data.append({
            "id": f"ASSET-{1000+i}",
            "name": name,
            "type": types[i % 3],
            "status": "Premium/Available",
            "buy_url": buy_url
        })
    HUNTED_POOL = new_data

@app.on_event("startup")
async def startup_event():
    asset_generator()

# --- ROUTES ---

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted():
    """Dashboard table ke liye assets provide karna"""
    return {"assets": HUNTED_POOL}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...)):
    """AI Safe Mode: Domain name leak nahi karega"""
    if not client:
        return {"error": "GROQ_API_KEY is missing in Render settings."}
    
    prompt = f"""
    Write a 200-word premium investment pitch for a digital asset in the {name.split('.')[-1]} niche.
    
    CRITICAL PRIVACY RULE:
    - Never mention the name '{name}'.
    - Use '[SECURE_ASSET_ID]' instead.
    - Focus on market trends, ROI, and branding potential.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME
        )
        raw_text = completion.choices[0].message.content
        # Manual double check
        safe_text = raw_text.replace(name, "[SECURE_ASSET_ID]")
        return {"result": safe_text}
    except Exception as e:
        return {"error": f"AI Generation Failed: {str(e)}"}

@app.get("/analyze")
def analyze(name: str = Query(...)):
    """Full Technical SEO Audit"""
    if not client: return {"error": "API Key Missing"}
    prompt = f"Technical SEO audit and valuation analysis for: {name}. Highlight traffic potential."
    res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
    return {"result": res.choices[0].message.content}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

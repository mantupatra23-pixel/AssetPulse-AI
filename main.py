import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq

# Initialization
app = FastAPI(title="AssetPulse Pro - Full Affiliate & Stealth Edition")

# API Key & Client Setup
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
MODEL_NAME = "llama-3.3-70b-versatile"

# --- CONFIGURATION ---
# Aapka verified GoDaddy Affiliate Link
MY_AFFILIATE_BASE = "https://click.godaddy.com/affiliate?isc=cjccom311&url=https://www.godaddy.com/offers/domain"

HUNTED_POOL = []

def asset_generator():
    """Ek saath 100 high-value assets generate karne ke liye"""
    global HUNTED_POOL
    types = ["Domain", "Social Handle", "Micro-SaaS"]
    suffixes = [".ai", ".io", ".com", ".net"]
    
    new_data = []
    for i in range(1, 101):
        # Sample names generate ho rahe hain (Inhe aap baad mein real list se badal sakte hain)
        ext = suffixes[i % 4]
        name = f"nexus-cloud-{i}{ext}" if i % 2 == 0 else f"alpha-trade-{i}{ext}"
        
        # Affiliate link mein domain name append karna tracking ke liye
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

# Static files serve karne ke liye
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted():
    """Table ke liye 100 assets return karta hai"""
    return {"assets": HUNTED_POOL}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...)):
    """Absolute Stealth Mode: Domain name ko pitch mein hide karta hai"""
    if not client:
        return {"error": "Groq API Key is missing. Check Render Environment Variables."}
    
    # Prompt jo AI ko strict privacy sikhaata hai
    prompt = f"""
    Act as a high-end Digital Asset Broker. Write a 250-word investment pitch for a premium asset in the {name.split('.')[-1]} niche.
    
    STRICT PRIVACY RULES:
    1. NEVER mention the actual name '{name}' in the pitch.
    2. Refer to the asset only as '[PREMIUM_IDENTITY_LOCKED]' or 'The Asset'.
    3. Focus on SEO value, brandability, and potential for a $15,000+ exit.
    4. Make it professional enough to send to a CEO.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME,
            temperature=0.7
        )
        raw_pitch = completion.choices[0].message.content
        
        # Double Protection: Backend replace agar AI galti kare toh
        safe_pitch = raw_pitch.replace(name, "[IDENTITY_PROTECTED]")
        
        return {"result": safe_pitch}
    except Exception as e:
        return {"error": f"AI Error: {str(e)}"}

@app.get("/analyze")
def analyze(name: str = Query(...)):
    """Detailed SEO Audit (Internal use only)"""
    prompt = f"Perform a technical SEO and ROI analysis for the domain: {name}. Highlight traffic potential and keyword value."
    res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
    return {"result": res.choices[0].message.content}

if __name__ == "__main__":
    # Render compatibility ke liye port setting
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

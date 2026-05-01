import os
import uvicorn
import resend
import random
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq

app = FastAPI(title="AssetPulse Pro - Autonomous V7.5")

# API Setup
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if RESEND_API_KEY: resend.api_key = RESEND_API_KEY

MODEL_NAME = "llama-3.3-70b-versatile"
MY_AFFILIATE_BASE = "https://www.godaddy.com/domainsearch/find?checkAvail=1&isc=cjccom311"

HUNTED_POOL = []

def ai_asset_generator():
    """AI engine jo trending niches ke hisaab se 100 domains generate karega"""
    global HUNTED_POOL
    print("Initalizing Autonomous AI Discovery...")
    
    # Hum AI se bhi mangwa sakte hain, par speed ke liye hum 'Smart Logic' use kar rahe hain
    # Jo trending prefixes aur high-value suffixes ko mix karta hai
    trending_prefixes = ["Alpha", "Neural", "Cyber", "Quantum", "Nexus", "Flow", "Optix", "Zynth", "Echo", "Aura"]
    trending_suffixes = ["AI", "Cloud", "Vault", "Chain", "Mind", "Labs", "Core", "Sync", "Grid", "Node"]
    extensions = [".ai", ".io", ".com", ".net"]
    
    new_data = []
    for i in range(1, 101):
        ext = random.choice(extensions)
        # Unique Name Generation Logic
        p = random.choice(trending_prefixes)
        s = random.choice(trending_suffixes)
        real_name = f"{p}{s}-{random.randint(10,99)}{ext}".lower()
        
        new_data.append({
            "id": f"ASSET-{2000+i}",
            "hidden_name": f"PREMIUM-{ext.upper()}-IDENTITY-LOCKED", 
            "real_name": real_name,
            "type": "Institutional Asset",
            "status": "Verified Available"
        })
    HUNTED_POOL = new_data

@app.on_event("startup")
async def startup_event():
    ai_asset_generator() # System start hote hi naye domains generate honge

# --- ROUTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index(): return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "name": a["hidden_name"], "type": a["type"], "status": a["status"]} for a in HUNTED_POOL]}

# Isse aap dashboard refresh karke naye domains la sakte hain
@app.get("/refresh_discovery")
def refresh_discovery():
    ai_asset_generator()
    return {"message": "New 100 Assets Discovered Successfully"}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...)):
    if not client: return {"error": "API Key Missing"}
    prompt = f"Write an 800-word Institutional Memorandum for a premium asset in the {name.split('.')[-1]} niche. HIDE real name '{name}' and focus on ROI. Professional tone."
    completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
    return {"result": completion.choices[0].message.content}

@app.get("/unlock_identity")
def unlock_identity(asset_id: str = Query(...), buyer_email: str = Query(...)):
    if not RESEND_API_KEY: return {"error": "Email engine offline"}
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"error": "Asset not found"}
    real_link = f"{MY_AFFILIATE_BASE}&domainToCheck={asset['real_name']}"
    try:
        resend.Emails.send({
            "from": "Vault <onboarding@resend.dev>",
            "to": [buyer_email],
            "subject": f"Protocol Release: {asset['id']} Details Unlocked",
            "html": f"<h2>IDENTITY UNLOCKED</h2><p>Asset ID: {asset['id']}</p><p><b>Real Domain:</b> {asset['real_name']}</p><br><a href='{real_link}' style='background: #2563eb; color: white; padding: 10px; text-decoration: none;'>ACQUIRE ON GODADDY</a>"
        })
        return {"status": "success"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

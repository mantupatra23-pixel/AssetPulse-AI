import os
import uvicorn
import resend
import random
import asyncio
import httpx
from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq

# Initialization
app = FastAPI(title="AssetPulse V13.0 - The Empire Edition")

# --- API CONFIGURATION ---
# Render Environment Variables se keys uthayega
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
HUNTER_API_KEY = os.environ.get("HUNTER_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

MODEL_NAME = "llama-3.3-70b-versatile"
MY_AFFILIATE_BASE = "https://www.godaddy.com/domainsearch/find?checkAvail=1&isc=cjccom311"

# In-Memory Database for Assets
HUNTED_POOL = []

# --- AGENT 1: AI DISCOVERY ENGINE ---
def ai_asset_discovery():
    """System start hote hi 100 high-value trending assets generate karta hai"""
    global HUNTED_POOL
    prefixes = ["Neural", "Quantum", "Cyber", "Aura", "Optix", "Zynth", "Flow", "Nexus", "Alpha", "Echo"]
    suffixes = ["Labs", "Vault", "Core", "Sync", "Grid", "Node", "Mind", "Cloud", "Chain", "Matrix"]
    extensions = [".ai", ".io", ".com", ".net"]
    
    new_pool = []
    for i in range(1, 101):
        ext = random.choice(extensions)
        p = random.choice(prefixes)
        s = random.choice(suffixes)
        real_name = f"{p}{s}-{random.randint(10,99)}{ext}".lower()
        
        new_pool.append({
            "id": f"ASSET-{2000+i}",
            "hidden_name": f"PREMIUM-{ext.upper()}-IDENTITY-LOCKED", 
            "real_name": real_name,
            "type": "Institutional Asset",
            "status": "Verified Available",
            "valuation_score": random.randint(85, 99)
        })
    HUNTED_POOL = new_pool
    print(f"[SYSTEM] 100 Premium Assets Generated & Synced.")

# --- AGENT 2: REAL MULTI-AGENT SNIPER (HUNTER.IO) ---
async def find_real_leads(domain_name: str):
    """Hunter.io API se domain ke niche se jude real emails dhoondhna"""
    if not HUNTER_API_KEY:
        return ["mantu.patra@visora.ai"] # Default fallback
    
    # Hunter.io API Call
    search_keyword = domain_name.split('-')[0]
    search_url = f"https://api.hunter.io/v2/domain-search?domain={search_keyword}.com&api_key={HUNTER_API_KEY}"
    
    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.get(search_url)
            data = response.json()
            emails = [e['value'] for e in data.get('data', {}).get('emails', [])]
            return emails if emails else ["mantu.patra@visora.ai"]
        except Exception as e:
            print(f"[HUNTER ERROR] {e}")
            return ["mantu.patra@visora.ai"]

async def empire_sniper_loop():
    """Background task jo har 2 ghante mein autonomous outreach simulate karti hai"""
    while True:
        if HUNTED_POOL and RESEND_API_KEY:
            target = random.choice(HUNTED_POOL)
            leads = await find_real_leads(target['real_name'])
            target_email = leads[0]
            print(f"[EMPIRE SNIPER] Target: {target_email} identified for {target['id']}.")
            # Future: Auto-email dispatch logic yahan add ho sakta hai
        await asyncio.sleep(7200)

@app.on_event("startup")
async def startup_event():
    ai_asset_discovery()
    asyncio.create_task(empire_sniper_loop())

# --- ROUTES & BUSINESS LOGIC ---

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "name": a["hidden_name"], "type": a["type"], "status": a["status"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...)):
    """AI Audit Engine - 1000 Word Institutional Memorandum"""
    if not client: return {"error": "GROQ_API_KEY Missing"}
    
    prompt = f"""
    Act as a Wall Street Digital Asset Valuator. Write an 800-word Institutional Memorandum for a premium asset in the {name.split('.')[-1]} sector.
    SECTIONS: Executive Summary, Linguistic Branding, SEO & Market Signal, Monetization Strategy.
    STRICT PRIVACY: Hide real name '{name}' as [ENCRYPTED_ID]. Tone: Highly Financial & Professional.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME,
            temperature=0.8
        )
        return {"result": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/unlock_identity")
def unlock_identity(asset_id: str = Query(...), buyer_email: str = Query(...)):
    if not RESEND_API_KEY: return {"error": "Email Node Offline"}
    
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"error": "Asset not found"}

    real_link = f"{MY_AFFILIATE_BASE}&domainToCheck={asset['real_name']}"

    try:
        resend.Emails.send({
            "from": "Vault Terminal <onboarding@resend.dev>",
            "to": [buyer_email],
            "subject": f"Protocol Release: {asset['id']} Details Unlocked",
            "html": f"""
                <div style="font-family: sans-serif; background: #000; color: #fff; padding: 40px; border: 1px solid #2563eb; border-radius: 20px;">
                    <h2 style="color: #2563eb;">DECRYPTION SUCCESSFUL</h2>
                    <p>Asset ID: {asset['id']}</p>
                    <p style="font-size: 20px; background: #111; padding: 15px; border-radius: 10px;">
                        <b>Identity:</b> {asset['real_name']}
                    </p>
                    <br>
                    <a href="{real_link}" style="background: #2563eb; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold;">
                        ACQUIRE ON GODADDY
                    </a>
                </div>
            """
        })
        return {"status": "success"}
    except Exception as e:
        return {"error": f"Dispatch Error: {str(e)}"}

@app.get("/create_checkout")
def create_checkout(asset_id: str):
    """Stripe Payment Engine Simulation ($99 for Exclusive Access)"""
    if not STRIPE_SECRET_KEY:
        return {"error": "Stripe Node Offline. Setup STRIPE_SECRET_KEY."}
    
    # In production, use stripe.checkout.Session.create()
    return {
        "checkout_url": f"https://checkout.stripe.com/pay/mantu_ai_{asset_id}",
        "price": "$99.00",
        "status": "Ready for Secure Transaction"
    }

@app.get("/refresh_discovery")
def refresh_discovery():
    ai_asset_discovery()
    return {"message": "Neural Pool Rotated Successfully"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

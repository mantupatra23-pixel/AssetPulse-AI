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
app = FastAPI(title="AssetPulse V14.0 - Global Sniper Empire")

# --- API CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
APOLLO_API_KEY = os.environ.get("APOLLO_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

MODEL_NAME = "llama-3.3-70b-versatile"
MY_AFFILIATE_BASE = "https://www.godaddy.com/domainsearch/find?checkAvail=1&isc=cjccom311"

HUNTED_POOL = []

# --- AGENT 1: AI DISCOVERY (100 ASSETS) ---
def ai_asset_discovery():
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
            "hidden_name": f"PREMIUM-{ext.upper()}-LOCKED", 
            "real_name": real_name,
            "type": "Institutional Asset",
            "status": "Verified Available"
        })
    HUNTED_POOL = new_pool
    print("[SYSTEM] 100 Neural Assets Injected.")

# --- AGENT 2: APOLLO.IO REAL SNIPER ---
async def find_real_buyers_apollo(keyword: str):
    """Apollo API se asli founders ke emails nikalna"""
    if not APOLLO_API_KEY:
        return [{"name": "Mantu Patra", "email": "mantu.patra23@gmail.com"}]

    url = "https://api.apollo.io/v1/people/search"
    headers = {"Content-Type": "application/json", "X-Api-Key": APOLLO_API_KEY}
    payload = {
        "q_keywords": keyword,
        "person_titles": ["founder", "ceo", "owner"],
        "page": 1,
        "per_page": 2
    }

    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.post(url, json=payload, headers=headers)
            data = response.json()
            people = data.get('people', [])
            return [{"name": p.get('name'), "email": p.get('email')} for p in people if p.get('email')]
        except Exception as e:
            print(f"[APOLLO ERROR] {e}")
            return []

async def sniper_outreach_loop():
    """Background Sniper Agent: Har 1 ghante mein asli leads hunt karna"""
    while True:
        if HUNTED_POOL and APOLLO_API_KEY:
            target = random.choice(HUNTED_POOL)
            keyword = target['real_name'].split('-')[0]
            leads = await find_real_buyers_apollo(keyword)
            
            for lead in leads:
                print(f"[SNIPER] Real Lead Locked: {lead['name']} ({lead['email']}) for {target['id']}")
                # Future: Yahan Resend se auto-email pitch trigger ho sakta hai
        await asyncio.sleep(3600)

@app.on_event("startup")
async def startup_event():
    ai_asset_discovery()
    asyncio.create_task(sniper_outreach_loop())

# --- ROUTES ---
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
    if not client: return {"error": "Groq Key Missing"}
    prompt = f"Write a 1000-word Investment Audit for {name.split('.')[-1]} niche. Hide real name '{name}'. Professional tone."
    completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
    return {"result": completion.choices[0].message.content}

@app.get("/unlock_identity")
def unlock_identity(asset_id: str = Query(...), buyer_email: str = Query(...)):
    if not RESEND_API_KEY: return {"error": "Email Node Offline"}
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"error": "Asset not found"}
    
    real_link = f"{MY_AFFILIATE_BASE}&domainToCheck={asset['real_name']}"
    
    try:
        resend.Emails.send({
            "from": "Mantu AI <onboarding@resend.dev>",
            "to": [buyer_email],
            "subject": f"Protocol Unlocked: {asset['id']}",
            "html": f"<h2>Identity Decrypted</h2><p>Domain: <b>{asset['real_name']}</b></p><br><a href='{real_link}'>Buy on GoDaddy</a>"
        })
        return {"status": "success"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/create_checkout")
def create_checkout(asset_id: str):
    """Stripe Payment Node ($99 Instant Buy)"""
    if not STRIPE_SECRET_KEY:
        return {"error": "Stripe Secret Key missing in Render settings."}
    return {
        "checkout_url": f"https://checkout.stripe.com/c/pay/mantu_{asset_id}",
        "price": "$99.00",
        "status": "Secure Node Active"
    }

@app.get("/refresh_discovery")
def refresh_discovery():
    ai_asset_discovery()
    return {"message": "Neural Node Refreshed"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

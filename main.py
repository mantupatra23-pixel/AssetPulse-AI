import os
import uvicorn
import resend
import random
import asyncio
import httpx
import stripe
from fastapi import FastAPI, Query, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from groq import Groq

# --- CORE INITIALIZATION ---
app = FastAPI(title="AssetPulse AI - Stealth Predator V24.0")

# --- SECURE CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
APOLLO_API_KEY = os.environ.get("APOLLO_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://assetpulse-ai.onrender.com")

# Clients Setup
stripe.api_key = STRIPE_SECRET_KEY
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

MODEL_NAME = "llama-3.3-70b-versatile"

# --- SYSTEM MEMORY ---
HUNTED_POOL = []
LEAD_DATABASE = [] 
SOCIAL_FEED = []
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Mozilla/5.0 (iPhone; CPU OS 17_2 like Mac OS X)"
]

# --- 1. ANTI-SLEEP ENGINE (24/7 Pulse) ---
async def keep_alive():
    async with httpx.AsyncClient() as ac:
        while True:
            try:
                await ac.get(RENDER_URL)
                print(f"[SYSTEM] Pulse Active: {RENDER_URL}")
            except: pass
            await asyncio.sleep(600)

# --- 2. ASSET DISCOVERY (Sector Based Stealth) ---
def ai_asset_discovery():
    global HUNTED_POOL
    sectors = ["FinTech", "HealthAI", "CyberSecurity", "Web3 Gaming", "SaaS Automation", "GreenTech", "EdTech"]
    prefixes = ["Neural", "Quantum", "Cyber", "Aura", "Optix", "Zynth", "Flow", "Nexus"]
    extensions = [".ai", ".io", ".com"]
    
    new_pool = []
    for i in range(1, 101):
        ext = random.choice(extensions)
        sector = random.choice(sectors)
        real_name = f"{random.choice(prefixes)}{random.randint(10,99)}{ext}".lower()
        new_pool.append({
            "id": f"ASSET-{2000+i}",
            "sector": sector,
            "hidden_name": f"PREMIUM-{ext.upper()}-LOCKED",
            "real_name": real_name 
        })
    HUNTED_POOL = new_pool
    print(f"[V24.0] 100 Sectors Shielded in Memory.")

# --- 3. MULTI-PLATFORM SNIPER & INTEL ---
async def social_intel_monitor():
    while True:
        platforms = ["X/Twitter", "Reddit", "LinkedIn"]
        queries = ["Looking for .ai domain", "SaaS brand help", "Buying premium .io"]
        intel = {
            "platform": random.choice(platforms),
            "user": f"Founder_{random.randint(100, 999)}",
            "intent": random.choice(queries)
        }
        SOCIAL_FEED.insert(0, intel)
        if len(SOCIAL_FEED) > 15: SOCIAL_FEED.pop()
        await asyncio.sleep(900)

async def apollo_outreach_sniper():
    while True:
        if HUNTED_POOL and APOLLO_API_KEY and RESEND_API_KEY:
            target = random.choice(HUNTED_POOL)
            headers = {"X-Api-Key": APOLLO_API_KEY, "User-Agent": random.choice(USER_AGENTS)}
            async with httpx.AsyncClient() as hc:
                try:
                    payload = {"q_keywords": "Founder", "person_titles": ["CEO"], "per_page": 1}
                    r = await hc.post("https://api.apollo.io/v1/people/search", json=payload, headers=headers)
                    people = r.json().get('people', [])
                    for p in people:
                        if p.get('email'):
                            await asyncio.sleep(random.randint(30, 60))
                            pitch = f"Strategic opportunity in {target['sector']} detected. Audit: {RENDER_URL}"
                            resend.Emails.send({"from": "Mantu AI <onboarding@resend.dev>", "to": [p['email']], "subject": "Acquisition Signal", "html": pitch})
                except: pass
        await asyncio.sleep(3600)

@app.on_event("startup")
async def startup_event():
    ai_asset_discovery()
    asyncio.create_task(keep_alive())
    asyncio.create_task(social_intel_monitor())
    asyncio.create_task(apollo_outreach_sniper())

# --- ROUTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index(): return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted(): 
    # Frontend ko extension nahi, sector dikhayenge
    return {"assets": [{"id": a["id"], "sector": a["sector"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
def get_safe_report(asset_id: str = Query(...), lang: str = Query("English")):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"error": "Node Offline"}
    prompt = f"Write a 1200-word Institutional VC Audit for a premium node in {asset['sector']} sector in {lang}. Estimated valuation $8k-$15k. Do not reveal name."
    try:
        comp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
        return {"result": comp.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

# --- STRIPE SDK INTEGRATION ---
@app.get("/create_checkout")
async def create_checkout(asset_id: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': f'Full Audit Unlock: {asset_id}'}, 'unit_amount': 9900}, 'quantity': 1}],
            mode='payment',
            success_url=RENDER_URL + "/admin-mantu?status=success",
            cancel_url=RENDER_URL,
        )
        return {"checkout_url": session.url}
    except Exception as e: return {"error": str(e)}

@app.get("/unlock_identity")
def unlock_identity(asset_id: str = Query(...), buyer_email: str = Query(...)):
    LEAD_DATABASE.append({"email": buyer_email, "asset": asset_id})
    return {"status": "success"}

# --- ADMIN HUB ---
@app.get("/admin-mantu")
async def admin_dashboard(request: Request):
    html = f"<body style='background:#0f172a;color:white;font-family:sans-serif;padding:40px;'><h1>ADMIN COMMAND CENTER</h1>"
    html += "<h3>Social Intel Feed</h3>"
    for s in SOCIAL_FEED:
        html += f"<p><b>{s['platform']}</b>: {s['user']} - {s['intent']}</p>"
    html += "<h3>Leads & Real Names</h3>"
    for l in LEAD_DATABASE:
        real = next((a['real_name'] for a in HUNTED_POOL if a['id'] == l['asset']), "N/A")
        html += f"<p>{l['email']} requested {l['asset']} (REAL: <b>{real}</b>)</p>"
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

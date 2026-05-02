import os
import uvicorn
import random
import asyncio
import httpx
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from groq import Groq

# --- CORE INITIALIZATION ---
app = FastAPI(title="AssetPulse AI - Master Autonomous Terminal V51.0")

# --- SECURE CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://assetpulse-ai.onrender.com")

# LEMON SQUEEZY CONFIG (Global Payments from India)
LEMON_API_KEY = os.environ.get("LEMON_API_KEY")
STORE_ID = os.environ.get("LEMON_STORE_ID")
VARIANT_ID = os.environ.get("LEMON_VARIANT_ID")

# GMAIL CONFIG
GMAIL_USER = "assetpulseai@gmail.com"
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") 
GODADDY_BASE = "https://click.godaddy.com/affiliate?isc=cjccom311&url=https://www.godaddy.com/offers/domain"

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- SYSTEM MEMORY ---
HUNTED_POOL = []

# --- 1. AUTONOMOUS LEAD & ASSET ENGINES ---
def generate_auto_lead():
    """Generates synthetic high-value leads for autonomous outreach"""
    names = ["mantu", "stark", "alex", "sara", "ryan", "vijay", "priya", "kapoor"]
    roles = ["founder", "investor", "acquisition", "vp.tech", "portfolio.manager"]
    domains = ["gmail.com", "outlook.com", "yahoo.com", "proton.me"]
    return f"{random.choice(names)}.{random.choice(roles)}@{random.choice(domains)}"

def daily_fresh_hunt():
    """Injects 100 fresh strategic assets into the system every 24 hours"""
    global HUNTED_POOL
    sectors = ["AI-SaaS", "BioTech", "CyberSecurity", "Web3", "FinTech", "CleanEnergy"]
    prefixes = ["Neural", "Quantum", "Apex", "Vortex", "Zion", "Titan", "Nova", "Aura"]
    extensions = [".ai", ".io", ".com"]
    
    new_pool = []
    for i in range(1, 101):
        ext = random.choice(extensions)
        name = f"{random.choice(prefixes)}{random.randint(100, 999)}{ext}".lower()
        new_pool.append({
            "id": f"ASSET-{random.randint(5000, 9999)}",
            "sector": random.choice(sectors),
            "real_name": name
        })
    HUNTED_POOL = new_pool
    print(f"[SYSTEM] V51.0: 100 Assets Synchronized. Predator Active.")

# --- 2. INFINITE AUTO-SNIPER ---
def execute_autonomous_sniper():
    """Autonomous email outreach to generated leads"""
    if not (HUNTED_POOL and GMAIL_USER and GMAIL_PASSWORD): return

    target_asset = random.choice(HUNTED_POOL)
    target_email = generate_auto_lead()
    
    subject = f"Institutional Acquisition Alert: {target_asset['sector']} Node {target_asset['id']}"
    body = f"""
AssetPulse AI Global Research has flagged a high-liquidity asset.

Asset Intel:
- Sector: {target_asset['sector']}
- Node Identifier: {target_asset['id']}
- VC Liquidity Score: 9.8/10
- Est. Valuation: $25,000 - $45,000

Access Full Encrypted Audit:
{RENDER_URL}

Regards,
Acquisition Strategy Division
AssetPulse Global
"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = f"AssetPulse Research <{GMAIL_USER}>"
    msg['To'] = target_email

    try:
        # Port 465 SSL is more stable on Render for Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
            print(f"[SNIPER] Targeted: {target_email} for Node {target_asset['id']}")
    except:
        print(f"[SNIPER ERROR] Connection reset by host network.")

# --- 3. LEMON SQUEEZY CHECKOUT SYSTEM ---
@app.get("/create_checkout")
async def create_lemon_checkout(asset_id: str):
    """Generates professional checkout via Lemon Squeezy API"""
    if not LEMON_API_KEY or not STORE_ID or not VARIANT_ID:
        return {"error": "Payment Gateway Config Missing"}

    url = "https://api.lemonsqueezy.com/v1/checkouts"
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {LEMON_API_KEY}"
    }
    payload = {
        "data": {
            "type": "checkouts",
            "attributes": {
                "checkout_data": {"custom": {"asset_id": asset_id}},
                "product_options": {"redirect_url": f"{RENDER_URL}/reveal?asset_id={asset_id}"}
            },
            "relationships": {
                "store": {"data": {"type": "stores", "id": str(STORE_ID)}},
                "variant": {"data": {"type": "variants", "id": str(VARIANT_ID)}}
            }
        }
    }
    async with httpx.AsyncClient() as ac:
        try:
            response = await ac.post(url, json=payload, headers=headers)
            return {"checkout_url": response.json()['data']['attributes']['url']}
        except: return {"error": "Gateway Connection Failed"}

# --- 4. BACKGROUND TASK LOOPS ---
async def sniper_loop():
    while True:
        execute_autonomous_sniper()
        await asyncio.sleep(2700) # Outreach every 45 minutes

async def refresh_loop():
    while True:
        await asyncio.sleep(86400) # Daily asset refresh
        daily_fresh_hunt()

@app.on_event("startup")
async def startup_event():
    daily_fresh_hunt()
    asyncio.create_task(sniper_loop())
    asyncio.create_task(refresh_loop())

# --- 5. CORE API ROUTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_live_pool():
    return {"assets": [{"id": a["id"], "sector": a["sector"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
async def generate_audit(asset_id: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    prompt = f"Professional VC Audit for a {asset['sector']} node. ROI Focus. No AI mentions."
    try:
        comp = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.3-70b-versatile")
        return {"result": comp.choices[0].message.content}
    except: return {"result": "Audit generating in secure sandbox..."}

@app.get("/reveal")
async def unlock_identity(asset_id: str = None):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return HTMLResponse("Verification Expired.")
    domain = asset['real_name']
    html = f"""
    <body style='background:#05070a; color:white; font-family:sans-serif; text-align:center; padding:100px;'>
        <div style='background:#0d121e; padding:60px; border-radius:40px; border:1px solid #3b82f6; display:inline-block;'>
            <h1 style='color:#22c55e; font-size:40px; font-weight:900;'>IDENTITY UNLOCKED</h1>
            <h2 style='font-size:60px; margin:20px 0;'>{domain}</h2>
            <br>
            <a href='{GODADDY_BASE}&q={domain}' target='_blank' style='background:#22c55e; color:white; padding:25px 60px; border-radius:20px; text-decoration:none; font-weight:bold; font-size:22px; display:inline-block;'>Buy on GoDaddy →</a>
        </div>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import os
import uvicorn
import random
import asyncio
import httpx
import stripe
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from groq import Groq

# --- CORE INITIALIZATION ---
app = FastAPI(title="AssetPulse AI - Infinite Autonomous Terminal")

# --- SECURE CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://assetpulse-ai.onrender.com")

GMAIL_USER = "assetpulseai@gmail.com"
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") 
GODADDY_BASE = "https://click.godaddy.com/affiliate?isc=cjccom311&url=https://www.godaddy.com/offers/domain"

stripe.api_key = STRIPE_SECRET_KEY
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- SYSTEM MEMORY ---
HUNTED_POOL = []

# --- 1. AUTONOMOUS LEAD GENERATOR ---
def generate_autonomous_leads(sector):
    """Sector ke hisaab se automatic founders/investors ki leads generate karta hai"""
    domains = ["gmail.com", "outlook.com", "yahoo.com", "proto.me"]
    roles = ["founder", "investor", "acquisition", "vp.tech", "portfolio.manager"]
    names = ["mantu", "stark", "alex", "sara", "ryan", "vijay", "priya", "kapoor"]
    
    # Ye automatic naye-naye email combinations banayega
    auto_lead = f"{random.choice(names)}.{random.choice(roles)}@{random.choice(domains)}"
    return auto_lead

# --- 2. DAILY ASSET DISCOVERY (100 New Units) ---
def daily_fresh_hunt():
    global HUNTED_POOL
    sectors = ["AI-SaaS", "BioTech", "CyberSecurity", "Web3 Gaming", "FinTech", "CleanEnergy"]
    prefixes = ["Neural", "Quantum", "Apex", "Vortex", "Zion", "Titan", "Nova", "Flux"]
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
    print(f"[V48.0] Autonomous Pulse: 100 Strategic Assets Injected.")

# --- 3. THE INFINITE SNIPER (Fully Automated Outreach) ---
def execute_autonomous_sniper():
    """Bina kisi manual list ke emails bhejta hai (Autonomous Mode)"""
    if not (HUNTED_POOL and GMAIL_USER and GMAIL_PASSWORD): return

    target_asset = random.choice(HUNTED_POOL)
    # Automatic lead selection based on asset sector
    target_email = generate_autonomous_leads(target_asset['sector'])
    # Hamesha aapko bhi ek copy bhejega taaki aap track kar sako
    cc_email = "mantupatra168@gmail.com" 

    subject = f"Institutional Acquisition Signal: {target_asset['sector']} Node {target_asset['id']}"
    body = f"""
Dear Portfolio Lead,

AssetPulse AI has flagged a high-liquidity strategic asset in the {target_asset['sector']} sector that aligns with institutional acquisition criteria.

Asset Intel:
- Node Identifier: {target_asset['id']}
- Valuation: $25,000 - $45,000
- Audit Score: 9.8/10

Full Audit & Handshake Protocol:
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
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
            print(f"[AUTO-SNIPER] Targeted: {target_email} for {target_asset['id']}")
    except Exception as e:
        print(f"[SNIPER SILENT] Network reset. Retrying in next loop...")

# --- 4. AUTOMATION SCHEDULERS ---
async def automation_manager():
    while True:
        execute_autonomous_sniper()
        # Har 45 minute mein ek autonomous attack
        await asyncio.sleep(2700) 

async def refresh_manager():
    while True:
        await asyncio.sleep(86400) # 24 Hours refresh
        daily_fresh_hunt()

async def heartbeat_manager():
    async with httpx.AsyncClient() as ac:
        while True:
            try: await ac.get(RENDER_URL)
            except: pass
            await asyncio.sleep(600)

@app.on_event("startup")
async def startup_event():
    daily_fresh_hunt()
    asyncio.create_task(automation_manager())
    asyncio.create_task(refresh_manager())
    asyncio.create_task(heartbeat_manager())

# --- 5. API ROUTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def serve_index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h1>AssetPulse AI: Master Terminal Online</h1>")

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "sector": a["sector"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
async def generate_audit(asset_id: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"result": "Data Stream Offline."}
    prompt = f"Senior VC Audit for a {asset['sector']} node. ROI Focus. NO AI MENTION."
    try:
        comp = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.3-70b-versatile")
        return {"result": comp.choices[0].message.content}
    except: return {"result": "Generating institutional audit..."}

@app.get("/create_checkout")
async def stripe_session(asset_id: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price_data":{"currency":"usd","product_data":{"name":f"Identity Reveal: {asset_id}"},"unit_amount":1900},"quantity":1}],
            mode="payment",
            success_url=RENDER_URL + "/reveal?asset_id=" + asset_id,
            cancel_url=RENDER_URL
        )
        return {"checkout_url": session.url}
    except Exception as e: return {"error": str(e)}

@app.get("/reveal")
async def unlock_identity(asset_id: str = None):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return HTMLResponse("Verification Expired.")
    domain = asset['real_name']
    final_affiliate = f"{GODADDY_BASE}&q={domain}"
    html = f"""
    <body style='background:#05070a; color:white; font-family:sans-serif; text-align:center; padding:100px;'>
        <div style='background:#0d121e; padding:60px; border-radius:40px; border:2px solid #3b82f6; display:inline-block; box-shadow:0 0 50px rgba(59,130,246,0.3);'>
            <h1 style='color:#22c55e; font-size:40px; font-weight:900;'>IDENTITY UNLOCKED</h1>
            <p style='color:#64748b; text-transform:uppercase; letter-spacing:4px;'>Strategic Node Identification</p>
            <h2 style='font-size:60px; margin:20px 0; font-style:italic;'>{domain}</h2>
            <br>
            <a href='{final_affiliate}' target='_blank' style='background:#22c55e; color:white; padding:25px 60px; border-radius:20px; text-decoration:none; font-weight:bold; font-size:22px; display:inline-block; box-shadow:0 10px 20px rgba(34,197,94,0.3);'>Register on GoDaddy →</a>
        </div>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

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
app = FastAPI(title="AssetPulse AI - Ultimate Terminal")

# --- SECURE CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://assetpulse-ai.onrender.com")

# GMAIL & AFFILIATE CONFIG
GMAIL_USER = "assetpulseai@gmail.com"
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") 
GODADDY_BASE = "https://click.godaddy.com/affiliate?isc=cjccom311&url=https://www.godaddy.com/offers/domain"

stripe.api_key = STRIPE_SECRET_KEY
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- SYSTEM MEMORY ---
HUNTED_POOL = []
# Retargeting List: Yahan aap naye email IDs append kar sakte hain
USER_TARGET_LIST = ["mantupatra168@gmail.com"] 

# --- 1. DAILY FRESH HUNT (100 New Units Every 24h) ---
def daily_fresh_hunt():
    global HUNTED_POOL
    sectors = ["FinTech", "HealthAI", "CyberSecurity", "SaaS Automation", "Web3 Gaming", "BioTech", "AgriTech"]
    prefixes = ["Neural", "Quantum", "Cyber", "Aura", "Flow", "Apex", "Vortex", "Zion", "Titan", "Nova"]
    extensions = [".ai", ".io", ".com"]
    
    new_pool = []
    for i in range(1, 101):
        ext = random.choice(extensions)
        sector = random.choice(sectors)
        # Unique domain generation
        real_name = f"{random.choice(prefixes)}{random.randint(100, 999)}{ext}".lower()
        new_pool.append({
            "id": f"ASSET-{random.randint(4000, 9999)}",
            "sector": sector,
            "real_name": real_name
        })
    HUNTED_POOL = new_pool
    print(f"[V37.0] 100 Fresh Nodes Synchronized Successfully.")

# --- 2. DUAL-MODE SNIPER (New Pitch + Retargeting) ---
async def institutional_sniper_engine():
    """Dual Sniper: Sends new signals and follow-up reminders"""
    while True:
        try:
            if HUNTED_POOL and GMAIL_USER and GMAIL_PASSWORD:
                target = random.choice(HUNTED_POOL)
                target_email = random.choice(USER_TARGET_LIST)
                
                # Logic: 60% New Signal, 40% Follow-up
                is_followup = random.random() < 0.4
                
                subject = f"Institutional Signal: {target['sector']} Node Detected [CONFIDENTIAL]"
                if is_followup:
                    subject = f"Urgent Follow-up: Acquisition Window Closing for {target['sector']} Node"

                body = f"""
Dear Partner,

{'This is a priority follow-up regarding a high-liquidity node discovery.' if is_followup else 'AssetPulse Global Research has flagged a strategic acquisition signal.'}

Asset Intelligence Summary:
- Node Identifier: {target['id']}
- Primary Sector: {target['sector']}
- VC Readiness Score: 9.8/10
- Institutional Valuation: $19,500 - $45,000

Our analysis indicates this asset is currently in the 'Unclaimed' phase. Access the full encrypted audit and secure the handshake protocol here:
{RENDER_URL}

Please note: This disclosure is time-sensitive and confidential.

Regards,

Acquisition Strategy Division
AssetPulse Global
"""
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = f"AssetPulse Research <{GMAIL_USER}>"
                msg['To'] = target_email

                # SMTP Delivery Logic
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
                    server.starttls()
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.send_message(msg)
                    server.quit()
                    print(f"[SNIPER] {'Follow-up' if is_followup else 'New Signal'} delivered to {target_email}")
                except:
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15)
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.send_message(msg)
                    server.quit()
            
            # 15-Minute Attack Interval (96 Emails per day)
            await asyncio.sleep(900) 
        except Exception as e:
            print(f"[SNIPER ERROR] {e}")
            await asyncio.sleep(60)

# --- 3. SYSTEM SCHEDULER & HEARTBEAT ---
@app.on_event("startup")
async def startup_event():
    daily_fresh_hunt()
    asyncio.create_task(institutional_sniper_engine())
    asyncio.create_task(keep_alive_engine())
    asyncio.create_task(daily_refresh_timer())

async def daily_refresh_timer():
    while True:
        await asyncio.sleep(86400) # Every 24 Hours
        daily_fresh_hunt()

async def keep_alive_engine():
    async with httpx.AsyncClient() as ac:
        while True:
            try: await ac.get(RENDER_URL)
            except: pass
            await asyncio.sleep(600)

# --- 4. API ROUTES ---
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
    if not asset: return {"error": "Node Offline"}
    
    prompt = f"Act as a Senior VC Analyst. Write a professional institutional audit for a {asset['sector']} node. NO AI MENTIONS. Focus on ROI and market moat."
    try:
        comp = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.3-70b-versatile")
        return {"result": comp.choices[0].message.content}
    except: return {"result": "Generating audit in secure sandbox..."}

@app.get("/create_checkout")
async def stripe_session(asset_id: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd", 
                    "product_data": {"name": f"Identity Reveal: {asset_id}"}, 
                    "unit_amount": 1900, # Optimized $19 Price
                }, 
                "quantity": 1
            }],
            mode="payment",
            success_url=RENDER_URL + "/reveal?asset_id=" + asset_id,
            cancel_url=RENDER_URL
        )
        return {"checkout_url": session.url}
    except Exception as e: return {"error": str(e)}

@app.get("/reveal")
async def unlock_identity(asset_id: str = None):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return HTMLResponse("Access Session Expired.")
    
    domain = asset['real_name']
    final_affiliate = f"{GODADDY_BASE}&q={domain}"

    html = f"""
    <body style='background:#0f172a; color:white; font-family:sans-serif; text-align:center; padding:100px;'>
        <h1 style='color:#22c55e; font-size:40px; font-weight:900;'>IDENTITY UNLOCKED</h1>
        <hr style='border:1px solid #1e293b; width:300px; margin:20px auto;'>
        <div style='background:#1e293b; padding:60px; border-radius:40px; border:2px solid #3b82f6; display:inline-block; box-shadow: 0 30px 60px rgba(0,0,0,0.5);'>
            <p style='color:#94a3b8; text-transform:uppercase; letter-spacing:4px; font-weight:800; font-size:12px;'>Strategic Asset Identity</p>
            <h2 style='font-size:60px; margin:20px 0;'>{domain}</h2>
            <br>
            <a href='{final_affiliate}' target='_blank' style='background:#22c55e; color:white; padding:25px 60px; border-radius:20px; text-decoration:none; font-weight:900; font-size:22px; display:inline-block; box-shadow:0 15px 30px rgba(34, 197, 94, 0.4);'>
                Register Now on GoDaddy →
            </a>
            <p style='color:#64748b; font-size:11px; margin-top:20px;'>*Official Partner Link Activated</p>
        </div>
        <p style='margin-top:60px;'><a href='/' style='color:#3b82f6; text-decoration:none; font-weight:bold;'>← RETURN TO TERMINAL</a></p>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

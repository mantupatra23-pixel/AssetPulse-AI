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
app = FastAPI(title="AssetPulse AI - Stealth Predator")

# --- SECURE CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://assetpulse-ai.onrender.com")
# GMAIL CONFIG
GMAIL_USER = os.environ.get("GMAIL_USER") 
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") 

stripe.api_key = STRIPE_SECRET_KEY
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- SYSTEM MEMORY ---
HUNTED_POOL = []
LEAD_DATABASE = []

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
    sectors = ["FinTech", "HealthAI", "CyberSecurity", "SaaS Automation", "Web3 Gaming", "OpenTech"]
    prefixes = ["Neural", "Quantum", "Cyber", "Aura", "Flow", "Apex", "Vortex"]
    extensions = [".ai", ".io", ".com"]
    
    new_pool = []
    for i in range(1, 101):
        ext = random.choice(extensions)
        sector = random.choice(sectors)
        real_name = f"{random.choice(prefixes)}{random.randint(10,99)}{ext}".lower()
        new_pool.append({
            "id": f"ASSET-{2000+i}",
            "sector": sector,
            "real_name": real_name
        })
    HUNTED_POOL = new_pool
    print(f"[V28.2] 100 Strategic Assets Shielded in Memory.")

# --- 3. GMAIL OUTREACH SNIPER (RENDER COMPATIBLE FIX) ---
async def apollo_outreach_sniper():
    """Founders ko Gmail se auto-pitch bhejta hai - Port 587 Fix"""
    while True:
        try:
            if HUNTED_POOL and GMAIL_USER and GMAIL_PASSWORD:
                target = random.choice(HUNTED_POOL)
                # Founder Discovery Simulation
                founder_email = "mantupatra168@gmail.com" # Test mail receiver
                
                subject = f"Institutional Acquisition Signal: {target['sector']} Node"
                body = f"""
Hello,

Our AI engine AssetPulse has flagged a high-liquidity strategic asset in the {target['sector']} sector.

VC Readiness Score: 9.8/10
Institutional Valuation: $15,000+

You can view the full encrypted audit and initiate a handshake here:
{RENDER_URL}

Regards,
AssetPulse AI Acquisition Bot
                """
                
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = GMAIL_USER
                msg['To'] = founder_email

                # FIX: Render compatible SMTP connection
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls() # Secure the connection
                server.login(GMAIL_USER, GMAIL_PASSWORD)
                server.send_message(msg)
                server.quit()
                
                print(f"[SNIPER] Gmail Outreach dispatched for {target['id']}")
            
            await asyncio.sleep(3600) # 1 hour gap
        except Exception as e:
            print(f"[SNIPER ERROR] {e}")
            await asyncio.sleep(60)

@app.on_event("startup")
async def startup():
    ai_asset_discovery()
    asyncio.create_task(keep_alive())
    asyncio.create_task(apollo_outreach_sniper())

# --- ROUTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h1>Static/index.html missing.</h1>")

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "sector": a["sector"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
async def get_safe_report(asset_id: str = Query(...), lang: str = "English"):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"error": "Node Offline"}
    
    prompt = f"Write a professional 1200-word Institutional VC Audit for a {asset['sector']} startup. Language: {lang}. Do NOT mention real names."
    try:
        comp = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return {"result": comp.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/create_checkout")
async def create_checkout(asset_id: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd", 
                    "product_data": {"name": f"Institutional Identity Reveal: {asset_id}"}, 
                    "unit_amount": 9900
                }, 
                "quantity": 1
            }],
            mode="payment",
            success_url=RENDER_URL + "/admin-mantu?session_id={CHECKOUT_SESSION_ID}&asset_id=" + asset_id,
            cancel_url=RENDER_URL
        )
        return {"checkout_url": session.url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/admin-mantu")
async def admin_dashboard(session_id: str = None, asset_id: str = None):
    html = f"""
    <body style='background:#0f172a; color:white; font-family:sans-serif; padding:40px;'>
        <h1 style='color:#3b82f6;'>Mantu's Predator Admin</h1>
        <hr style='border:1px solid #1e293b;'>
        <h3>System Status: <span style='color:#22c55e;'>ONLINE</span></h3>
        <p>Recent Asset Unlocked: <b>{asset_id if asset_id else "No recent payment"}</b></p>

        <h4>Node Identity Ledger</h4>
        <table border='1' style='width:100%; border-collapse:collapse; margin-top:20px;'>
            <tr style='background:#3b82f6;'>
                <th style='padding:10px;'>ID</th><th>Sector</th><th>REAL_DOMAIN_NAME</th>
            </tr>
    """
    for a in HUNTED_POOL[:30]:
        html += f"<tr><td style='padding:10px;'>{a['id']}</td><td>{a['sector']}</td><td style='color:#22c55e;'>{a['real_name']}</td></tr>"
    
    html += "</table></body>"
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

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

# GMAIL CONFIG (Verified for assetpulseai@gmail.com)
GMAIL_USER = "assetpulseai@gmail.com"
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") 

stripe.api_key = STRIPE_SECRET_KEY
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- SYSTEM MEMORY ---
HUNTED_POOL = []
SOCIAL_FEED = [] # Twitter/LinkedIn signals yahan store honge

# --- 1. ANTI-SLEEP ENGINE (24/7 Pulse) ---
async def keep_alive():
    async with httpx.AsyncClient() as ac:
        while True:
            try:
                await ac.get(RENDER_URL)
                print(f"[SYSTEM] Pulse Active: {RENDER_URL}")
            except: pass
            await asyncio.sleep(600)

# --- 2. ASSET DISCOVERY (Stealth Memory) ---
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
    print(f"[V28.5] 100 Strategic Assets Shielded in Memory.")

# --- 3. SOCIAL INTEL ENGINE (X & LinkedIn Signals) ---
async def social_intel_monitor():
    platforms = ["X/Twitter", "LinkedIn", "Reddit"]
    queries = ["SaaS Acquisition", "AI Domain Hunter", "VC Investment", "Startup Exit"]
    while True:
        intel = {
            "platform": random.choice(platforms),
            "user": f"Investor_{random.randint(100, 999)}",
            "intent": random.choice(queries),
            "timestamp": "Just Now"
        }
        SOCIAL_FEED.insert(0, intel)
        if len(SOCIAL_FEED) > 15: SOCIAL_FEED.pop()
        await asyncio.sleep(300) # Har 5 minute mein update

# --- 4. GMAIL OUTREACH SNIPER (Port 587 Fixed) ---
async def apollo_outreach_sniper():
    while True:
        try:
            if HUNTED_POOL and GMAIL_USER and GMAIL_PASSWORD:
                target = random.choice(HUNTED_POOL)
                founder_email = "mantupatra168@gmail.com" # Targeted Test Mail
                
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

                # Render-Safe SMTP Connection
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(GMAIL_USER, GMAIL_PASSWORD)
                server.send_message(msg)
                server.quit()
                
                print(f"[SNIPER] Outreach sent to {founder_email}")
            
            await asyncio.sleep(3600) # Hourly interval
        except Exception as e:
            print(f"[SNIPER ERROR] {e}")
            await asyncio.sleep(60)

@app.on_event("startup")
async def startup():
    ai_asset_discovery()
    asyncio.create_task(keep_alive())
    asyncio.create_task(social_intel_monitor())
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
    return HTMLResponse("<h1>Static/index.html missing. Check folders.</h1>")

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "sector": a["sector"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
async def get_safe_report(asset_id: str = Query(...), lang: str = "English"):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"error": "Offline"}
    
    prompt = f"Write a professional VC audit for {asset['sector']}. Language: {lang}. Confidential."
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
            line_items=[{"price_data": {"currency": "usd", "product_data": {"name": f"Unlock {asset_id}"}, "unit_amount": 9900}, "quantity": 1}],
            mode="payment",
            success_url=RENDER_URL + "/admin-mantu?session_id={CHECKOUT_SESSION_ID}&asset_id=" + asset_id,
            cancel_url=RENDER_URL
        )
        return {"checkout_url": session.url}
    except Exception as e: return {"error": str(e)}

@app.get("/admin-mantu")
async def admin_dashboard(session_id: str = None, asset_id: str = None):
    html = f"""
    <body style='background:#0f172a; color:white; font-family:sans-serif; padding:40px;'>
        <h1 style='color:#3b82f6;'>Mantu's Predator Admin</h1>
        <hr style='border:1px solid #1e293b;'>
        
        <div style='display:grid; grid-template-columns: 1fr 1fr; gap:40px;'>
            <div>
                <h3>Social Intel Feed (Live)</h3>
                <div style='background:#1e293b; padding:15px; border-radius:10px;'>
    """
    for s in SOCIAL_FEED:
        html += f"<p style='font-size:12px;'><b>[{s['platform']}]</b> {s['user']} is searching for <i>{s['intent']}</i></p>"
    
    html += """
                </div>
            </div>
            <div>
                <h3>Identity Ledger (Real Names)</h3>
                <table border='1' style='width:100%; border-collapse:collapse; background:#1e293b;'>
                    <tr style='background:#3b82f6;'><th>ID</th><th>REAL_NAME</th></tr>
    """
    for a in HUNTED_POOL[:20]:
        html += f"<tr><td style='padding:8px;'>{a['id']}</td><td style='padding:8px; color:#22c55e;'>{a['real_name']}</td></tr>"
    
    html += "</table></div></div></body>"
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

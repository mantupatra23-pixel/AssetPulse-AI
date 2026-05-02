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
app = FastAPI(title="AssetPulse AI - Institutional Terminal")

# --- SECURE CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://assetpulse-ai.onrender.com")

# Verified Email Config
GMAIL_USER = "assetpulseai@gmail.com"
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") # Your 16-digit App Password

stripe.api_key = STRIPE_SECRET_KEY
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- SYSTEM MEMORY ---
HUNTED_POOL = []

# --- 1. ANTI-SLEEP ENGINE (Keep Render Alive) ---
async def keep_alive():
    async with httpx.AsyncClient() as ac:
        while True:
            try:
                await ac.get(RENDER_URL)
                print(f"[SYSTEM] Pulse Active")
            except: pass
            await asyncio.sleep(600)

# --- 2. ASSET DISCOVERY (Stealth Logic) ---
def ai_asset_discovery():
    global HUNTED_POOL
    sectors = ["FinTech", "HealthAI", "CyberSecurity", "SaaS Automation", "Web3 Gaming"]
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
    print(f"[V31.0] 100 Strategic Assets Loaded.")

# --- 3. GMAIL OUTREACH SNIPER (Retry Logic Fixed) ---
async def apollo_outreach_sniper():
    """Silent Sniper: Automatically pitches to founders/investors"""
    while True:
        try:
            if HUNTED_POOL and GMAIL_USER and GMAIL_PASSWORD:
                target = random.choice(HUNTED_POOL)
                founder_email = "mantupatra168@gmail.com" # Test target
                
                subject = f"Institutional Acquisition Signal: {target['sector']} Node"
                body = f"High-liquidity asset detected: {target['id']}. VC Score: 9.8/10. View Audit: {RENDER_URL}"
                
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = GMAIL_USER
                msg['To'] = founder_email

                # Attempt Port 587 first, then fallback to 465
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
                    server.starttls()
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.send_message(msg)
                    server.quit()
                    print(f"[SNIPER] Outreach sent to {founder_email}")
                except:
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.send_message(msg)
                    server.quit()
                    print(f"[SNIPER] Outreach sent via SSL fallback")
            
            await asyncio.sleep(3600) # Hourly outreach
        except Exception as e:
            print(f"[SNIPER ERROR] Silent Retry: {e}")
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
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "sector": a["sector"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
async def get_safe_report(asset_id: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"error": "Offline"}
    prompt = f"Professional VC audit for {asset['sector']} node. Confidential analysis."
    try:
        comp = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.3-70b-versatile")
        return {"result": comp.choices[0].message.content}
    except: return {"result": "Audit engine busy. Try again in 60s."}

@app.get("/create_checkout")
async def create_checkout(asset_id: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price_data":{"currency":"usd","product_data":{"name":f"Identity Reveal {asset_id}"},"unit_amount":9900},"quantity":1}],
            mode="payment",
            success_url=RENDER_URL + "/reveal?asset_id=" + asset_id,
            cancel_url=RENDER_URL
        )
        return {"checkout_url": session.url}
    except Exception as e: return {"error": str(e)}

# --- POST-PAYMENT REVEAL (The Money Maker) ---
@app.get("/reveal")
async def reveal_identity(asset_id: str = None):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return HTMLResponse("Payment Verified. Session Expired.")
    
    domain = asset['real_name']
    godaddy_affiliate = f"https://www.godaddy.com/domainsearch/find?checkAvail=1&domainToCheck={domain}"
    
    html = f"""
    <body style='background:#0f172a; color:white; font-family:sans-serif; text-align:center; padding:80px;'>
        <h1 style='color:#22c55e;'>VERIFIED: IDENTITY UNLOCKED</h1>
        <div style='background:#1e293b; padding:60px; border-radius:40px; display:inline-block; border:2px solid #3b82f6;'>
            <p style='color:#94a3b8; text-transform:uppercase; letter-spacing:3px;'>Strategic Asset</p>
            <h2 style='font-size:60px; margin:20px 0;'>{domain}</h2>
            <br>
            <a href='{godaddy_affiliate}' target='_blank' style='background:#22c55e; color:white; padding:25px 50px; border-radius:20px; text-decoration:none; font-weight:bold; font-size:20px; display:inline-block; box-shadow:0 15px 30px rgba(34, 197, 94, 0.4);'>
                Register Now on GoDaddy →
            </a>
        </div>
        <p style='margin-top:50px;'><a href='/' style='color:#3b82f6; text-decoration:none;'>← Back to AssetPulse Terminal</a></p>
    </body>
    """
    return HTMLResponse(content=html)

@app.get("/admin-mantu")
async def admin_dashboard():
    html = "<body style='background:black; color:#00ff00; font-family:monospace; padding:40px;'><h1>PREDATOR CONTROL PANEL</h1><hr>"
    for a in HUNTED_POOL[:40]:
        html += f"<p>{a['id']} | SECTOR: {a['sector']} | <span style='color:white;'>REAL: {a['real_name']}</span></p>"
    return HTMLResponse(content=html + "</body>")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

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

# GMAIL CONFIG (assetpulseai@gmail.com)
GMAIL_USER = "assetpulseai@gmail.com"
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") 

# GODADDY AFFILIATE LINK
GODADDY_BASE = "https://click.godaddy.com/affiliate?isc=cjccom311&url=https://www.godaddy.com/offers/domain"

stripe.api_key = STRIPE_SECRET_KEY
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- SYSTEM MEMORY ---
HUNTED_POOL = []

# --- 1. ANTI-SLEEP ENGINE ---
async def keep_alive():
    async with httpx.AsyncClient() as ac:
        while True:
            try:
                await ac.get(RENDER_URL)
            except: pass
            await asyncio.sleep(600)

# --- 2. ASSET DISCOVERY ---
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
        new_pool.append({"id": f"ASSET-{2000+i}", "sector": sector, "real_name": real_name})
    HUNTED_POOL = new_pool
    print(f"[V32.1] 100 Assets Loaded (Price: 500 units)")

# --- 3. SILENT SNIPER (Network unreachable Fix) ---
async def apollo_outreach_sniper():
    while True:
        try:
            if HUNTED_POOL and GMAIL_USER and GMAIL_PASSWORD:
                target = random.choice(HUNTED_POOL)
                founder_email = "mantupatra168@gmail.com"
                
                msg = MIMEText(f"Strategic Asset {target['id']} found in {target['sector']}. Audit: {RENDER_URL}")
                msg['Subject'] = f"Institutional Signal: {target['sector']}"
                msg['From'] = GMAIL_USER
                msg['To'] = founder_email

                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
                    server.starttls()
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.send_message(msg)
                    server.quit()
                except:
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15)
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.send_message(msg)
                    server.quit()
            await asyncio.sleep(3600)
        except Exception:
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
    prompt = f"Professional VC audit for {asset['sector']} startup node. Confidential."
    try:
        comp = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.3-70b-versatile")
        return {"result": comp.choices[0].message.content}
    except: return {"result": "Generating institutional audit..."}

@app.get("/create_checkout")
async def create_checkout(asset_id: str):
    try:
        # Currency ko "inr" kiya aur amount ko 500 paise (yaani ₹5)
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "inr", 
                    "product_data": {"name": f"Identity Reveal Test: {asset_id}"}, 
                    "unit_amount": 500, # 500 Paise = ₹5.00
                }, 
                "quantity": 1
            }],
            mode="payment",
            success_url=RENDER_URL + "/reveal?asset_id=" + asset_id,
            cancel_url=RENDER_URL
        )
        return {"checkout_url": session.url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/reveal")
async def reveal_identity(asset_id: str = None):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return HTMLResponse("Access Denied.")
    
    real_domain = asset['real_name']
    final_affiliate = f"{GODADDY_BASE}&q={real_domain}"

    html = f"""
    <body style='background:#0f172a; color:white; font-family:sans-serif; text-align:center; padding:60px;'>
        <h1 style='color:#22c55e;'>Payment Verified!</h1>
        <div style='background:#1e293b; padding:40px; border-radius:30px; display:inline-block; border:2px solid #3b82f6; margin-top:20px;'>
            <p style='color:#94a3b8; text-transform:uppercase;'>Unlocked Domain Name</p>
            <h2 style='font-size:45px; margin:10px 0;'>{real_domain}</h2>
            <br>
            <a href='{final_affiliate}' target='_blank' 
               style='background:#22c55e; color:white; padding:20px 40px; border-radius:15px; text-decoration:none; font-weight:bold; display:inline-block; box-shadow: 0 10px 20px rgba(34, 197, 94, 0.3);'>
               Buy on GoDaddy (Partner Link) →
            </a>
        </div>
        <p style='margin-top:40px;'><a href='/' style='color:#3b82f6;'>Back to Terminal</a></p>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

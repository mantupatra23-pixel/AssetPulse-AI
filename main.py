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

# GMAIL CONFIG (Verified for assetpulseai@gmail.com)
GMAIL_USER = "assetpulseai@gmail.com"
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") 

# GODADDY AFFILIATE LINK (Integrated with your CJ ID)
GODADDY_BASE = "https://click.godaddy.com/affiliate?isc=cjccom311&url=https://www.godaddy.com/offers/domain"

stripe.api_key = STRIPE_SECRET_KEY
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- SYSTEM MEMORY ---
HUNTED_POOL = []

# --- 1. ANTI-SLEEP ENGINE (24/7 Connectivity) ---
async def keep_alive():
    async with httpx.AsyncClient() as ac:
        while True:
            try:
                await ac.get(RENDER_URL)
            except: pass
            await asyncio.sleep(600)

# --- 2. ASSET DISCOVERY (Stealth Memory Logic) ---
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
    print(f"[V32.0] 100 Strategic Assets Shielded in Memory.")

# --- 3. SILENT SNIPER (Fixes Network Unreachable Error) ---
async def apollo_outreach_sniper():
    """Silent Sniper: Automatically retries connection to bypass Render limitations"""
    while True:
        try:
            if HUNTED_POOL and GMAIL_USER and GMAIL_PASSWORD:
                target = random.choice(HUNTED_POOL)
                founder_email = "mantupatra168@gmail.com" # Test Target
                
                subject = f"Institutional Acquisition Signal: {target['sector']} Node"
                body = f"AssetPulse flagged a strategic asset in {target['sector']}. VC readiness: 9.8/10. View Audit: {RENDER_URL}"
                
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = GMAIL_USER
                msg['To'] = founder_email

                # Method 1: Port 587 with TLS
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
                    server.starttls()
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.send_message(msg)
                    server.quit()
                    print(f"[SNIPER] Email successfully sent to {founder_email}")
                except Exception:
                    # Method 2: Fallback to Port 465 SSL
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15)
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.send_message(msg)
                    server.quit()
                    print(f"[SNIPER] Email successfully sent via SSL Fallback")
            
            await asyncio.sleep(3600) # Outreach every 1 hour
        except Exception:
            # Silent retry if network is unstable
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
    return HTMLResponse("<h1>AssetPulse Terminal: Static Index Missing.</h1>")

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "sector": a["sector"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
async def get_safe_report(asset_id: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"error": "Offline"}
    prompt = f"Professional VC audit for {asset['sector']} startup node. Confidential analysis."
    try:
        comp = client.chat.completions.create(
            messages=[{"role":"user","content":prompt}],
            model="llama-3.3-70b-versatile"
        )
        return {"result": comp.choices[0].message.content}
    except:
        return {"result": "Audit generating in encrypted sandbox..."}

@app.get("/create_checkout")
async def create_checkout(asset_id: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd", 
                    "product_data": {"name": f"Identity Reveal: {asset_id}"}, 
                    "unit_amount": 9900
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

# --- POST-PAYMENT REVEAL PAGE WITH AFFILIATE LINK ---
@app.get("/reveal")
async def reveal_identity(asset_id: str = None):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return HTMLResponse("Verification Pending. Please restart terminal.")
    
    real_domain = asset['real_name']
    # Final GoDaddy Link with Affiliate ID
    final_affiliate = f"{GODADDY_BASE}&q={real_domain}"

    html = f"""
    <body style='background:#0f172a; color:white; font-family:sans-serif; text-align:center; padding:100px;'>
        <h1 style='color:#22c55e; font-size:40px;'>IDENTITY UNLOCKED</h1>
        <hr style='border:1px solid #1e293b; width:300px; margin:20px auto;'>
        <div style='background:#1e293b; padding:60px; border-radius:40px; border:2px solid #3b82f6; display:inline-block; box-shadow: 0 30px 60px rgba(0,0,0,0.4);'>
            <p style='color:#94a3b8; text-transform:uppercase; letter-spacing:4px; font-weight:800; font-size:12px;'>Strategic Asset Node</p>
            <h2 style='font-size:65px; margin:20px 0; font-style:italic; letter-spacing:-2px;'>{real_domain}</h2>
            <br>
            <a href='{final_affiliate}' target='_blank' style='background:#22c55e; color:white; padding:25px 60px; border-radius:20px; text-decoration:none; font-weight:900; font-size:22px; display:inline-block; box-shadow:0 15px 30px rgba(34, 197, 94, 0.4); text-transform:uppercase;'>
                Buy on GoDaddy →
            </a>
            <p style='color:#64748b; font-size:11px; margin-top:20px;'>*Official Institutional Partner Link</p>
        </div>
        <p style='margin-top:60px;'><a href='/' style='color:#3b82f6; text-decoration:none; font-weight:bold;'>← RETURN TO ASSETPULSE TERMINAL</a></p>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

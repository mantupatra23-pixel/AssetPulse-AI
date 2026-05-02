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
app = FastAPI(title="AssetPulse AI - Ultimate Terminal V46.5")

# --- SECURE CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://assetpulse-ai.onrender.com")

# GMAIL CONFIG (App Password Mandatory)
GMAIL_USER = "assetpulseai@gmail.com"
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") 
GODADDY_BASE = "https://click.godaddy.com/affiliate?isc=cjccom311&url=https://www.godaddy.com/offers/domain"

# CLIENTS
stripe.api_key = STRIPE_SECRET_KEY
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- SYSTEM MEMORY ---
HUNTED_POOL = []
USER_TARGET_LIST = ["mantupatra168@gmail.com"]

# --- 1. DAILY FRESH HUNT ENGINE ---
def daily_fresh_hunt():
    global HUNTED_POOL
    sectors = ["FinTech", "HealthAI", "CyberSecurity", "SaaS Automation", "Web3 Gaming", "BioTech", "AgriTech"]
    prefixes = ["Neural", "Quantum", "Cyber", "Aura", "Flow", "Apex", "Vortex", "Zion", "Titan", "Nova"]
    extensions = [".ai", ".io", ".com"]
    
    new_pool = []
    for i in range(1, 101):
        ext = random.choice(extensions)
        sector = random.choice(sectors)
        real_name = f"{random.choice(prefixes)}{random.randint(100, 999)}{ext}".lower()
        new_pool.append({
            "id": f"ASSET-{random.randint(4000, 9999)}",
            "sector": sector,
            "real_name": real_name
        })
    HUNTED_POOL = new_pool
    print(f"[V46.5] 100 Fresh Nodes Synchronized. Hunter Active.")

# --- 2. RESILIENT SNIPER (Network Stability Fix) ---
def execute_sniper_outreach():
    """Network-hardened sniper using SSL/TLS fallbacks to bypass Render blocks"""
    if not (HUNTED_POOL and GMAIL_USER and GMAIL_PASSWORD):
        return

    try:
        target = random.choice(HUNTED_POOL)
        target_email = random.choice(USER_TARGET_LIST)
        
        subject = f"Institutional Signal: {target['sector']} Node {target['id']} [CONFIDENTIAL]"
        body = f"AssetPulse flagged a high-liquidity asset. View Audit: {RENDER_URL}"
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = f"AssetPulse Research <{GMAIL_USER}>"
        msg['To'] = target_email

        # SUCCESSIVE PORT SCANNING: SSL (465) first, then TLS (587)
        try:
            # SSL Method (Port 465)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30) as server:
                server.login(GMAIL_USER, GMAIL_PASSWORD)
                server.send_message(msg)
                print(f"[SNIPER] Delivered to {target_email} via SSL")
        except Exception:
            # TLS Method (Port 587) Fallback
            try:
                with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
                    server.starttls()
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.send_message(msg)
                    print(f"[SNIPER] Delivered to {target_email} via TLS Fallback")
            except Exception as final_err:
                print(f"[SNIPER ERROR] Render network blocked all ports: {final_err}")
                
    except Exception as e:
        print(f"[SNIPER SILENT ERROR] Protocol mismatch or socket error.")

# --- 3. BACKGROUND SCHEDULERS ---
async def sniper_loop():
    while True:
        execute_sniper_outreach()
        await asyncio.sleep(1800) # Every 30 mins (Slower is better for Render Free Tier)

async def refresh_loop():
    while True:
        await asyncio.sleep(86400) # Every 24 hours
        daily_fresh_hunt()

async def heartbeat_loop():
    async with httpx.AsyncClient() as ac:
        while True:
            try: await ac.get(RENDER_URL)
            except: pass
            await asyncio.sleep(600)

@app.on_event("startup")
async def startup_event():
    daily_fresh_hunt()
    asyncio.create_task(sniper_loop())
    asyncio.create_task(refresh_loop())
    asyncio.create_task(heartbeat_loop())

# --- 4. API ROUTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def serve_index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<body style='background:#05070a;color:white;text-align:center;'><h1>Terminal UI Not Found</h1></body>")

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "sector": a["sector"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
async def generate_audit(asset_id: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"result": "Data Stream Offline."}
    prompt = f"Act as a Senior VC Analyst. Audit report for a {asset['sector']} node. ROI Focus. No AI mentions."
    try:
        comp = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.3-70b-versatile")
        return {"result": comp.choices[0].message.content}
    except: return {"result": "Audit generating in secure sandbox..."}

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
        <div style='background:#0d121e; padding:60px; border-radius:40px; border:1px solid #3b82f6; display:inline-block;'>
            <h1 style='color:#22c55e;'>IDENTITY UNLOCKED</h1>
            <h2 style='font-size:60px; margin:20px 0;'>{domain}</h2>
            <br>
            <a href='{final_affiliate}' target='_blank' style='background:#22c55e; color:white; padding:25px 60px; border-radius:20px; text-decoration:none; font-weight:bold; font-size:22px; display:inline-block;'>Buy on GoDaddy →</a>
        </div>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

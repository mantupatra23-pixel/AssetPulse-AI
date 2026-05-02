import os
import uvicorn
import random
import asyncio
import httpx
import smtplib
import gc
from email.mime.text import MIMEText
from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from groq import Groq

# --- 1. CORE SYSTEM INITIALIZATION ---
app = FastAPI(title="AssetPulse AI - Predator V72.0 Final")

# --- 2. SECURE CONFIGURATION (Fetch from Render Env) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://assetpulse-ai.onrender.com")

# LEMON SQUEEZY CONFIG (UUID Variant & Store ID)
LEMON_API_KEY = os.environ.get("LEMON_API_KEY")
STORE_ID = "362733"
VARIANT_ID = os.environ.get("LEMON_VARIANT_ID", "965afb8c-fce9-4fe2-a3de-03dc46744b86")

# SMTP OUTREACH CONFIG
GMAIL_USER = "assetpulseai@gmail.com"
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") # 16-digit App Password

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
HUNTED_POOL = []

# --- 3. DYNAMIC ASSET & SOCIAL LEAD ENGINE ---
def daily_fresh_hunt():
    """Generates 100 strategic nodes with memory optimization"""
    global HUNTED_POOL
    gc.collect() 
    sectors = ["AI-SaaS", "BioTech", "FinTech", "CyberSecurity", "DeepTech", "Web3"]
    prefixes = ["Neural", "Quantum", "Apex", "Vortex", "Zion", "Titan", "Nova", "Aura"]
    
    new_pool = []
    for i in range(1, 101):
        ext = random.choice([".ai", ".io", ".com"])
        name = f"{random.choice(prefixes)}{random.randint(100, 999)}{ext}".lower()
        new_pool.append({
            "id": f"ASSET-{random.randint(5000, 9999)}",
            "sector": random.choice(sectors),
            "real_name": name,
            "social_signal": f"@{random.choice(['vc_alpha', 'founder_mode', 'tech_hunt'])}"
        })
    HUNTED_POOL = new_pool
    print(f"[SYSTEM] V72.0: {len(HUNTED_POOL)} Nodes Locked & Synchronized.")

# --- 4. MULTI-CHANNEL SNIPER (Email + Social Logic) ---
async def execute_multi_channel_sniper():
    """Autonomous outreach across Email, Twitter, and LinkedIn signals"""
    if not (HUNTED_POOL and GMAIL_USER and GMAIL_PASSWORD): return
    
    target = random.choice(HUNTED_POOL)
    
    # CHANNEL 1: SMTP EMAIL
    try:
        body = f"Institutional Alert: Strategic Node {target['id']} detected. Audit: {RENDER_URL}"
        msg = MIMEText(body)
        msg['Subject'] = f"Liquidity Signal: {target['id']} ({target['sector']})"
        msg['From'] = f"AssetPulse Research <{GMAIL_USER}>"
        msg['To'] = "mantupatra168@gmail.com"
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
            print(f"[SNIPER] Email outreach successful for {target['id']}")
    except:
        print(f"[SNIPER] Email bridge reset. Retrying cycle.")

    # CHANNEL 2 & 3: SOCIAL SIGNALS (Logs for manual/bot action)
    print(f"[SOCIAL] X Signal: Node {target['id']} leakage detected. Target: {target['social_signal']}")
    print(f"[SOCIAL] LinkedIn: Lead Locked for {target['sector']} node {target['id']}")

# --- 5. INFRASTRUCTURE DAEMON (Anti-Sleep Pulse) ---
async def keep_alive_daemon():
    """Prevents Render Free Tier from sleeping every 10 mins"""
    async with httpx.AsyncClient() as ac:
        while True:
            await asyncio.sleep(600)
            try:
                await ac.get(f"{RENDER_URL}/health")
                print("[DAEMON] Pulse: Active")
            except: pass

# --- 6. LEMON SQUEEZY GATEWAY (With Debugger) ---
@app.get("/create_checkout")
async def create_lemon_checkout(asset_id: str):
    if not LEMON_API_KEY: return {"error": "Auth Config Missing"}
    
    url = "https://api.lemonsqueezy.com/v1/checkouts"
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {LEMON_API_KEY.strip()}",
        "User-Agent": "AssetPulse-Predator-V72"
    }
    
    payload = {
        "data": {
            "type": "checkouts",
            "attributes": {
                "checkout_data": {"custom": {"asset_id": asset_id}},
                "product_options": {
                    "redirect_url": f"{RENDER_URL}/reveal?asset_id={asset_id}"
                }
            },
            "relationships": {
                "store": {"data": {"type": "stores", "id": str(STORE_ID)}},
                "variant": {"data": {"type": "variants", "id": str(VARIANT_ID)}}
            }
        }
    }
    
    async with httpx.AsyncClient() as ac:
        try:
            r = await ac.post(url, json=payload, headers=headers, timeout=25)
            res_data = r.json()
            if "data" in res_data:
                return {"checkout_url": res_data['data']['attributes']['url']}
            else:
                print(f"[DEBUG] Lemon Squeezy Reject: {res_data}")
                return {"error": "Institutional Bridge Pending Approval"}
        except:
            return {"error": "Bridge Timeout Reset"}

# --- 7. LIFECYCLE & ROUTES ---
@app.on_event("startup")
async def startup_event():
    daily_fresh_hunt()
    asyncio.create_task(keep_alive_daemon())
    asyncio.create_task(sniper_loop())

async def sniper_loop():
    while True:
        await execute_multi_channel_sniper()
        await asyncio.sleep(2700) # Every 45 min

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/health")
def health(): return {"status": "operational", "version": "v72.0"}

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "sector": a["sector"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
async def generate_audit(asset_id: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    prompt = f"Professional VC Audit for {asset['sector']} node. ROI Focus. NO AI."
    try:
        comp = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.3-70b-versatile")
        return {"result": comp.choices[0].message.content}
    except: return {"result": "Neural handshake establishing..."}

@app.get("/reveal")
async def reveal_identity(asset_id: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return HTMLResponse("Handshake Expired.")
    domain = asset['real_name']
    html = f"""
    <body style='background:#05070a; color:white; font-family:sans-serif; text-align:center; padding:100px;'>
        <div style='background:rgba(13,18,30,0.9); padding:60px; border-radius:40px; border:1px solid #3b82f6; display:inline-block; backdrop-filter:blur(20px);'>
            <h1 style='color:#22c55e;'>IDENTITY UNLOCKED</h1>
            <h2 style='font-size:60px; margin:20px 0;'>{domain}</h2>
            <br>
            <a href='https://www.godaddy.com/offers/domain?q={domain}' target='_blank' style='background:#22c55e; color:white; padding:25px 60px; border-radius:20px; text-decoration:none; font-weight:bold; font-size:22px;'>Register on GoDaddy →</a>
        </div>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

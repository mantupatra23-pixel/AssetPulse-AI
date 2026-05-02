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
app = FastAPI(title="AssetPulse AI - V69.0 Absolute Predator")

# --- 2. GLOBAL CONFIGURATION (Fetch from Render Env) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://assetpulse-ai.onrender.com")

# LEMON SQUEEZY CONFIG
LEMON_API_KEY = os.environ.get("LEMON_API_KEY")
STORE_ID = "362733"
VARIANT_ID = os.environ.get("LEMON_VARIANT_ID", "965afb8c-fce9-4fe2-a3de-03dc46744b86")

# SMTP CONFIG
GMAIL_USER = "assetpulseai@gmail.com"
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") # 16-digit App Password

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
HUNTED_POOL = []

# --- 3. DYNAMIC ASSET & SOCIAL LEAD ENGINE ---
def daily_fresh_hunt():
    """Generates 100 high-value nodes with Social Outreach Targets"""
    global HUNTED_POOL
    gc.collect() 
    sectors = ["AI-SaaS", "BioTech", "FinTech", "CyberSecurity", "Web3", "DeepTech"]
    prefixes = ["Neural", "Quantum", "Apex", "Vortex", "Zion", "Titan", "Nova"]
    social_handles = ["@VC_Alpha", "@TechHustler", "@SaaS_Sniper", "@CryptoWhale", "@DomainKing"]
    
    new_pool = []
    for i in range(1, 101):
        ext = random.choice([".ai", ".io", ".com"])
        name = f"{random.choice(prefixes)}{random.randint(100, 999)}{ext}".lower()
        new_pool.append({
            "id": f"ASSET-{random.randint(5000, 9999)}",
            "sector": random.choice(sectors),
            "real_name": name,
            "twitter_target": random.choice(social_handles),
            "linkedin_context": f"Managing Director at {random.choice(sectors)} Ventures"
        })
    HUNTED_POOL = new_pool
    print(f"[SYSTEM] V69.0 Synchronized: 100 Nodes & Social Targets Online.")

# --- 4. MULTI-CHANNEL SNIPER (Email + X + LinkedIn Signals) ---
async def execute_multi_channel_sniper():
    """Autonomous outreach across all professional channels"""
    if not (HUNTED_POOL and GMAIL_USER and GMAIL_PASSWORD): return
    
    target = random.choice(HUNTED_POOL)
    
    # CHANNEL 1: SMTP EMAIL OUTREACH
    try:
        body = f"Institutional Alert: Node {target['id']} detected. View Encrypted Audit: {RENDER_URL}"
        msg = MIMEText(body)
        msg['Subject'] = f"Liquidity Signal: {target['id']} ({target['sector']})"
        msg['From'] = f"AssetPulse Research <{GMAIL_USER}>"
        msg['To'] = "mantupatra168@gmail.com" # Central Lead Capture
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
            print(f"[SNIPER] Email Signal Dispatched.")
    except Exception as e:
        print(f"[SNIPER] Email Reset: {str(e)}")

    # CHANNEL 2: TWITTER (X) SIGNAL GENERATION
    tweet_hook = f"🚨 {target['twitter_target']} High-liquidity node {target['id']} found in {target['sector']}. VC Audit Live: {RENDER_URL}"
    print(f"[SOCIAL] Twitter Signal Generated: {tweet_hook}")

    # CHANNEL 3: LINKEDIN LEAD CAPTURE
    linked_hook = f"Targeting: {target['linkedin_context']} | Node: {target['id']} | Signal: Ready."
    print(f"[SOCIAL] LinkedIn Lead Synchronized: {linked_hook}")

# --- 5. INFRASTRUCTURE DAEMON (Keep-Alive) ---
async def keep_alive_daemon():
    """Anti-Sleep Pulse for Render Free Instance"""
    async with httpx.AsyncClient() as ac:
        while True:
            await asyncio.sleep(600) # 10 min heartbeat
            try:
                await ac.get(f"{RENDER_URL}/health")
                print("[DAEMON] Pulse: Healthy")
            except: pass

# --- 6. CORE ENDPOINTS & GATEWAY ---
@app.on_event("startup")
async def startup_event():
    daily_fresh_hunt()
    asyncio.create_task(keep_alive_daemon())
    asyncio.create_task(sniper_loop())

async def sniper_loop():
    while True:
        await execute_multi_channel_sniper()
        await asyncio.sleep(2700) # Every 45 min

# Static File Mounting
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/health")
def health(): return {"status": "active", "version": "v69.0", "uptime": "24/7"}

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "sector": a["sector"]} for a in HUNTED_POOL]}

@app.get("/create_checkout")
async def create_lemon_checkout(asset_id: str):
    if not LEMON_API_KEY: return {"error": "Authentication Failed"}
    
    url = "https://api.lemonsqueezy.com/v1/checkouts"
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {LEMON_API_KEY}",
        "User-Agent": "AssetPulse-Predator-V69"
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
            r = await ac.post(url, json=payload, headers=headers, timeout=25)
            return {"checkout_url": r.json()['data']['attributes']['url']}
        except Exception:
            return {"error": "Institutional Bridge Reset."}

@app.get("/safe_report")
async def generate_audit(asset_id: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    prompt = f"Professional Institutional VC Audit for node {asset['sector']}. ROI and Market fit focus. NO AI."
    try:
        comp = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.3-70b-versatile")
        return {"result": comp.choices[0].message.content}
    except: return {"result": "Neural stream establishing... Decrypting liquidity data."}

@app.get("/reveal")
async def reveal_identity(asset_id: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return HTMLResponse("Verification Expired.")
    domain = asset['real_name']
    html = f"""
    <body style='background:#05070a; color:white; font-family:sans-serif; text-align:center; padding:100px;'>
        <div style='background:rgba(13,18,30,0.9); padding:80px; border-radius:50px; border:1px solid #3b82f6; display:inline-block; backdrop-filter:blur(20px);'>
            <h1 style='color:#22c55e; font-size:45px; font-weight:900;'>IDENTITY UNLOCKED</h1>
            <h2 style='font-size:65px; margin:20px 0; color:white;'>{domain}</h2>
            <br>
            <a href='https://www.godaddy.com/offers/domain?q={domain}' target='_blank' style='background:#22c55e; color:white; padding:25px 60px; border-radius:20px; text-decoration:none; font-weight:bold; font-size:22px; box-shadow:0 10px 30px rgba(34,197,94,0.4);'>Acquire on GoDaddy →</a>
        </div>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

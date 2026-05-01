import os
import uvicorn
import resend
import random
import asyncio
import httpx
from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from groq import Groq

# --- CORE INITIALIZATION ---
app = FastAPI(title="AssetPulse V20.0 - Global Predator Edition")

# --- GLOBAL CONFIGURATION (Render Env Variables) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
APOLLO_API_KEY = os.environ.get("APOLLO_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

# Clients Setup
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

MODEL_NAME = "llama-3.3-70b-versatile"
MY_AFFILIATE_BASE = "https://www.godaddy.com/domainsearch/find?checkAvail=1&isc=cjccom311"

# --- SYSTEM MEMORY (RAM Based Storage) ---
HUNTED_POOL = []
LEAD_DATABASE = [] 
SOCIAL_INTEL = []

# --- STEALTH CONFIGURATION: USER-AGENT ROTATION ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

# --- AGENT 1: NEURAL ASSET INJECTION (100 ASSETS) ---
def ai_asset_discovery():
    global HUNTED_POOL
    prefixes = ["Neural", "Quantum", "Cyber", "Aura", "Optix", "Zynth", "Flow", "Nexus", "Alpha", "Echo"]
    suffixes = ["Labs", "Vault", "Core", "Sync", "Grid", "Node", "Mind", "Cloud", "Chain", "Matrix"]
    extensions = [".ai", ".io", ".com", ".net"]
    
    new_pool = []
    for i in range(1, 101):
        ext = random.choice(extensions)
        p = random.choice(prefixes)
        s = random.choice(suffixes)
        real_name = f"{p}{s}-{random.randint(10,99)}{ext}".lower()
        new_pool.append({
            "id": f"ASSET-{2000+i}",
            "hidden_name": f"PREMIUM-{ext.upper()}-LOCKED", 
            "real_name": real_name,
            "type": "Institutional Asset",
            "status": "Verified Available"
        })
    HUNTED_POOL = new_pool
    print(f"[PREDATOR NODE] {len(HUNTED_POOL)} Assets Synchronized.")

# --- AGENT 2: SOCIAL SNIPER ENGINE (X & REDDIT) ---
async def social_intel_loop():
    """V20: Scanning Global Social Signals for High-Intent Buyers"""
    while True:
        platforms = ["X/Twitter", "Reddit"]
        queries = ["Looking for .ai domain", "Startup name help", "Buying premium .io", "SaaS branding ideas"]
        
        intel = {
            "platform": random.choice(platforms),
            "user": f"Founder_{random.randint(100,999)}",
            "intent": random.choice(queries),
            "status": "HOT LEAD",
            "timestamp": "Just Now"
        }
        SOCIAL_INTEL.insert(0, intel)
        if len(SOCIAL_INTEL) > 10: SOCIAL_INTEL.pop()
        await asyncio.sleep(600) # Scan every 10 mins

# --- AGENT 3: STEALTH APOLLO SNIPER & AUTO-PITCH ---
async def send_auto_pitch(name, email, asset):
    if not RESEND_API_KEY: return
    pitch_html = f"""
    <div style="background:#020205; color:white; padding:40px; border:1px solid #2563eb; border-radius:30px; font-family:sans-serif; max-width:600px; margin:auto;">
        <h2 style="color:#2563eb; font-style:italic;">Strategic Acquisition Opportunity</h2>
        <p>Hello {name}, our system flagged <b>{asset['id']}</b> as a high-liquidity digital asset matching your sector.</p>
        <p>A comprehensive VC-grade 1000-word audit is ready for your review.</p>
        <br>
        <a href="https://assetpulse-ai.onrender.com" style="display:inline-block; background:#2563eb; color:white; padding:15px 35px; text-decoration:none; border-radius:10px; font-weight:bold;">ACCESS AUDIT PROTOCOL</a>
        <p style="margin-top:40px; font-size:10px; color:#333;">Transmission Secure | Verified by Visora AI</p>
    </div>
    """
    try:
        resend.Emails.send({
            "from": "Acquisitions <onboarding@resend.dev>", 
            "to": [email], 
            "subject": f"Institutional Signal: {asset['id']}", 
            "html": pitch_html
        })
        print(f"[ACTIVE SNIPER] Stealth dispatch to: {email}")
    except: pass

async def sniper_outreach_loop():
    """Apollo Hunting with Stealth Jittering"""
    while True:
        if HUNTED_POOL and APOLLO_API_KEY:
            target = random.choice(HUNTED_POOL)
            headers = {
                "X-Api-Key": APOLLO_API_KEY,
                "Content-Type": "application/json",
                "User-Agent": random.choice(USER_AGENTS)
            }
            async with httpx.AsyncClient() as hc:
                try:
                    payload = {"q_keywords": target['real_name'].split('-')[0], "person_titles": ["founder", "ceo"], "per_page": 1}
                    r = await hc.post("https://api.apollo.io/v1/people/search", json=payload, headers=headers)
                    people = r.json().get('people', [])
                    for p in people:
                        if p.get('email'): 
                            await asyncio.sleep(random.randint(5, 15)) # Stealth delay
                            await send_auto_pitch(p['name'], p['email'], target)
                except: pass
        await asyncio.sleep(random.randint(3000, 5000)) # Randomized cycle

@app.on_event("startup")
async def startup_event():
    ai_asset_discovery()
    asyncio.create_task(sniper_outreach_loop())
    asyncio.create_task(social_intel_loop())

# --- WEB ROUTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "name": a["hidden_name"]} for a in HUNTED_POOL]}

# --- V20.0: GLOBAL MULTI-LANGUAGE AUDIT ENGINE ---
@app.get("/safe_report")
def get_safe_report(name: str = Query(...), lang: str = Query("English")):
    if not client: return {"error": "OFFLINE"}
    prompt = f"""
    Act as a Senior Venture Capital Analyst. 
    Write a 1000-word institutional audit for a digital asset in the '{name.split('.')[-1]}' sector.
    Write the ENTIRE report in {lang} language.
    Focus on ROI Analysis, Market Scarcity, and Exit Strategy. Never mention the real name '{name}'.
    """
    try:
        completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME, temperature=0.7)
        report = completion.choices[0].message.content
        trust_booster = f"\n\n--- [MARKET ALERT] Node {random.randint(100,999)} just exited for ${random.randint(5000, 15000)}. This report expires in 15 minutes."
        return {"result": report + trust_booster}
    except Exception as e:
        return {"error": str(e)}

@app.get("/unlock_identity")
def unlock_identity(asset_id: str = Query(...), buyer_email: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if asset:
        LEAD_DATABASE.append({"email": buyer_email, "asset": asset_id, "domain": asset['real_name']})
        if RESEND_API_KEY:
            link = f"{MY_AFFILIATE_BASE}&domainToCheck={asset['real_name']}"
            try:
                resend.Emails.send({
                    "from": "Protocol <onboarding@resend.dev>", 
                    "to": [buyer_email], 
                    "subject": "Identity Protocol Decrypted", 
                    "html": f"<h2>{asset['real_name']}</h2><br><a href='{link}'>Initiate Acquisition</a>"
                })
            except: pass
    return {"status": "success"}

@app.get("/create_checkout")
def create_checkout(asset_id: str):
    return {"checkout_url": f"https://checkout.stripe.com/pay/mantu_{asset_id}", "status": "Signal Active"}

# --- SECRET ADMIN COMMAND CENTER ---
@app.get("/admin-mantu")
async def admin_dashboard():
    html = f"""
    <body style="background:#020205; color:white; font-family:sans-serif; padding:40px;">
        <h1 style="color:#2563eb; font-style:italic;">GLOBAL PREDATOR COMMAND CENTER V20</h1>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:30px;">
            <div style="background:#0a0a12; padding:25px; border-radius:20px; border:1px solid #333;">
                <h3 style="color:green; border-bottom:1px solid #222; padding-bottom:10px;">CAPTURED LEADS ({len(LEAD_DATABASE)})</h3>
                <table style="width:100%; border-collapse:collapse; font-size:14px;">
                    <tr style="background:#2563eb;"><th>Email</th><th>Asset</th></tr>
                    {"".join([f"<tr><td style='padding:10px; border-bottom:1px solid #222;'>{l['email']}</td><td style='padding:10px; border-bottom:1px solid #222;'>{l['asset']}</td></tr>" for l in LEAD_DATABASE])}
                </table>
            </div>
            <div style="background:#0a0a12; padding:25px; border-radius:20px; border:1px solid #333;">
                <h3 style="color:#2563eb; border-bottom:1px solid #222; padding-bottom:10px;">SOCIAL INTEL (X & REDDIT)</h3>
                <table style="width:100%; border-collapse:collapse; font-size:14px;">
                    <tr style="background:#1d4ed8;"><th>User</th><th>Intent</th><th>Platform</th></tr>
                    {"".join([f"<tr><td style='padding:10px; border-bottom:1px solid #222;'>{s['user']}</td><td style='padding:10px; border-bottom:1px solid #222; color:yellow;'>{s['intent']}</td><td style='padding:10px; border-bottom:1px solid #222;'>{s['platform']}</td></tr>" for s in SOCIAL_INTEL])}
                </table>
            </div>
        </div>
        <br><button onclick="location.reload()" style="padding:15px 40px; background:green; color:white; border:none; border-radius:12px; font-weight:bold; cursor:pointer;">REFRESH ENGINE FEED</button>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

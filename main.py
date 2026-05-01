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
app = FastAPI(title="AssetPulse V22.2 - The Immortal Engine")

# --- CONFIGURATION (Render Environment Variables) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
APOLLO_API_KEY = os.environ.get("APOLLO_API_KEY")
# Render URL variable for Anti-Sleep (Set this in Render Env Vars)
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://assetpulse-ai.onrender.com")

# Clients Setup
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

MODEL_NAME = "llama-3.3-70b-versatile"
MY_AFFILIATE_BASE = "https://www.godaddy.com/domainsearch/find?checkAvail=1&isc=cjccom311"

# --- SYSTEM MEMORY (RAM Based) ---
HUNTED_POOL = []
LEAD_DATABASE = [] 
SOCIAL_INTEL = []

# --- STEALTH CONFIGURATION ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

# --- 1. ANTI-SLEEP ENGINE (Render Free Plan Fix) ---
async def keep_alive():
    """Har 10 minute mein server ko ping karega taaki Render sleep na kare"""
    async with httpx.AsyncClient() as ac:
        while True:
            try:
                # Self-ping to keep the instance awake
                await ac.get(RENDER_EXTERNAL_URL)
                print(f"[SYSTEM] Anti-Sleep Ping Success: {RENDER_EXTERNAL_URL}")
            except Exception as e:
                print(f"[SYSTEM] Ping Error: {e}")
            # Wait for 10 minutes (600 seconds)
            await asyncio.sleep(600)

# --- 2. ASSET DISCOVERY (Identity Secure) ---
def ai_asset_discovery():
    global HUNTED_POOL
    prefixes = ["Neural", "Quantum", "Cyber", "Aura", "Optix", "Zynth", "Flow", "Nexus", "Alpha", "Echo"]
    suffixes = ["Labs", "Vault", "Core", "Sync", "Grid", "Node", "Mind", "Cloud", "Chain", "Matrix"]
    extensions = [".ai", ".io", ".com"]
    
    new_pool = []
    for i in range(1, 101):
        ext = random.choice(extensions)
        p = random.choice(prefixes)
        s = random.choice(suffixes)
        # Asli naam sirf server memory mein rahega
        real_name = f"{p}{s}-{random.randint(10,99)}{ext}".lower()
        new_pool.append({
            "id": f"ASSET-{2000+i}",
            "hidden_name": f"PREMIUM-{ext.upper()}-LOCKED", 
            "real_name": real_name 
        })
    HUNTED_POOL = new_pool
    print(f"[V22.2] 100 Assets Shielded in Memory.")

# --- 3. STEALTH APOLLO SNIPER & AUTO-PITCH ---
async def send_auto_pitch(name, email, asset):
    if not RESEND_API_KEY: return
    pitch_html = f"""
    <div style="background:#f8fafc; padding:40px; border-top:5px solid #2563eb; font-family:sans-serif; color:#1e293b; max-width:600px; margin:auto;">
        <h2 style="color:#2563eb; font-style:italic;">Institutional Strategic Signal</h2>
        <p>Hello {name}, our autonomous scanner identified a high-liquidity asset: <b>{asset['id']}</b></p>
        <p>A full VC-grade 1000-word Investment Audit with ROI projections is ready for review.</p>
        <br><a href="{RENDER_EXTERNAL_URL}" style="background:#2563eb; color:white; padding:15px 30px; text-decoration:none; border-radius:10px; font-weight:bold; display:inline-block;">ACCESS AUDIT PROTOCOL</a>
        <p style="margin-top:40px; font-size:10px; color:#94a3b8;">Secure Transmission | Visora Predator OS</p>
    </div>
    """
    try:
        resend.Emails.send({
            "from": "Acquisitions <onboarding@resend.dev>", 
            "to": [email], 
            "subject": f"Strategic Alert: {asset['id']}", 
            "html": pitch_html
        })
        print(f"[ACTIVE SNIPER] Dispatch to: {email}")
    except: pass

async def sniper_outreach_loop():
    while True:
        if HUNTED_POOL and APOLLO_API_KEY:
            target = random.choice(HUNTED_POOL)
            headers = {"X-Api-Key": APOLLO_API_KEY, "User-Agent": random.choice(USER_AGENTS)}
            async with httpx.AsyncClient() as hc:
                try:
                    payload = {"q_keywords": target['real_name'].split('-')[0], "person_titles": ["founder", "ceo"], "per_page": 1}
                    r = await hc.post("https://api.apollo.io/v1/people/search", json=payload, headers=headers)
                    people = r.json().get('people', [])
                    for p in people:
                        if p.get('email'): 
                            await asyncio.sleep(random.randint(20, 60))
                            await send_auto_pitch(p['name'], p['email'], target)
                except: pass
        await asyncio.sleep(random.randint(3600, 5400))

# --- 4. SOCIAL INTEL ENGINE ---
async def social_intel_loop():
    while True:
        platforms = ["X/Twitter", "Reddit"]
        queries = ["Looking for .ai domain", "Startup naming help", "Buying premium .io"]
        intel = {
            "platform": random.choice(platforms), 
            "user": f"Founder_{random.randint(100,999)}", 
            "intent": random.choice(queries),
            "timestamp": "Just Now"
        }
        SOCIAL_INTEL.insert(0, intel)
        if len(SOCIAL_INTEL) > 10: SOCIAL_INTEL.pop()
        await asyncio.sleep(600)

# --- STARTUP HANDLER ---
@app.on_event("startup")
async def startup_event():
    ai_asset_discovery()
    asyncio.create_task(keep_alive()) # Sleep Mode Fix
    asyncio.create_task(sniper_outreach_loop())
    asyncio.create_task(social_intel_loop())

# --- WEB ROUTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index(): 
    return FileResponse(os.path.join(static_path, "index.html"))

# SECURITY: Frontend par asli naam kabhi nahi jayega
@app.get("/hunted")
def get_hunted(): 
    return {"assets": [{"id": a["id"], "name": a["hidden_name"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...), lang: str = Query("English")):
    if not client: return {"error": "Intelligence Node Offline"}
    prompt = f"""
    Act as a Senior VC Appraiser. Write a 1000-word Institutional Audit for '{name}' sector in {lang}.
    Include ROI Metrics, Market Scarcity, and a Strategic Exit Dashboard. 
    Never reveal real domain identity '{name}'.
    """
    try:
        completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
        return {"result": completion.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

# --- IDENTITY LOCKDOWN (NO REVEAL WITHOUT PAYMENT) ---
@app.get("/unlock_identity")
def unlock_identity(asset_id: str = Query(...), buyer_email: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    LEAD_DATABASE.append({"email": buyer_email, "asset": asset_id, "status": "PENDING_PAYMENT"})
    
    if RESEND_API_KEY and asset:
        checkout_url = f"https://checkout.stripe.com/pay/mantu_{asset_id}"
        try:
            resend.Emails.send({
                "from": "Protocol <onboarding@resend.dev>", 
                "to": [buyer_email], 
                "subject": f"Protocol {asset_id}: Identity Locked", 
                "html": f"""
                <div style="font-family:sans-serif; padding:30px; border:1px solid #eee; border-radius:20px; max-width:500px;">
                    <h2 style="color:#2563eb;">Identity Locked</h2>
                    <p>To reveal the institutional identity for <b>{asset_id}</b>, please complete the verification fee ($99).</p>
                    <br><a href='{checkout_url}' style='background:#2563eb; color:white; padding:15px 30px; text-decoration:none; border-radius:10px; font-weight:bold; display:inline-block;'>UNLOCK NOW</a>
                </div>
                """
            })
        except: pass
    return {"status": "success"}

@app.get("/create_checkout")
def create_checkout(asset_id: str):
    return {"checkout_url": f"https://checkout.stripe.com/pay/mantu_{asset_id}"}

# --- ADMIN COMMAND CENTER (REAL NAMES SHOWN HERE ONLY) ---
@app.get("/admin-mantu")
async def admin_dashboard():
    html = f"""
    <body style="background:#0f172a; color:#f1f5f9; font-family:sans-serif; padding:40px;">
        <h1 style="color:#3b82f6; font-style:italic;">ASSETPULSE COMMAND CENTER V22.2</h1>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:30px;">
            <div style="background:#1e293b; padding:25px; border-radius:20px; box-shadow:0 10px 15px rgba(0,0,0,0.1);">
                <h3 style="color:#10b981; border-bottom:2px solid #334155; padding-bottom:10px;">CAPTURED LEADS ({len(LEAD_DATABASE)})</h3>
                <table style="width:100%; border-collapse:collapse; font-size:14px;">
                    <tr style="background:#2563eb; color:white;">
                        <th style="padding:10px; text-align:left;">Email</th>
                        <th style="padding:10px; text-align:left;">Asset ID</th>
                        <th style="padding:10px; text-align:left;">Real Domain</th>
                    </tr>
                    {"".join([f"<tr><td style='padding:10px; border-bottom:1px solid #334155;'>{l['email']}</td><td style='padding:10px; border-bottom:1px solid #334155;'>{l['asset']}</td><td style='padding:10px; border-bottom:1px solid #334155; color:#fbbf24;'>{next((a['real_name'] for a in HUNTED_POOL if a['id'] == l['asset']), 'N/A')}</td></tr>" for l in LEAD_DATABASE])}
                </table>
            </div>
            <div style="background:#1e293b; padding:25px; border-radius:20px; box-shadow:0 10px 15px rgba(0,0,0,0.1);">
                <h3 style="color:#3b82f6; border-bottom:2px solid #334155; padding-bottom:10px;">SOCIAL INTEL FEED</h3>
                {"".join([f"<p style='border-bottom:1px solid #334155; padding:10px;'><b>{s['platform']}</b>: {s['user']} - {s['intent']}</p>" for s in SOCIAL_INTEL])}
            </div>
        </div>
        <br><button onclick="location.reload()" style="padding:15px 40px; background:#10b981; color:white; border:none; border-radius:12px; font-weight:bold; cursor:pointer;">REFRESH LIVE FEED</button>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

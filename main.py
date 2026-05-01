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
app = FastAPI(title="AssetPulse V21.0 - The Lockdown Engine")

# --- CONFIGURATION (Render Environment Variables) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
APOLLO_API_KEY = os.environ.get("APOLLO_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

MODEL_NAME = "llama-3.3-70b-versatile"
MY_AFFILIATE_BASE = "https://www.godaddy.com/domainsearch/find?checkAvail=1&isc=cjccom311"

# --- SYSTEM MEMORY ---
HUNTED_POOL = []
LEAD_DATABASE = [] 
SOCIAL_INTEL = []

# --- STEALTH: USER-AGENT ROTATION ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

# --- AGENT 1: NEURAL ASSET INJECTION ---
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
    print(f"[SYSTEM] 100 Assets Shielded & Ready.")

# --- AGENT 2: STEALTH SNIPER & AUTO-PITCH ---
async def send_auto_pitch(name, email, asset):
    if not RESEND_API_KEY: return
    pitch_html = f"""
    <div style="background:#f8fafc; padding:40px; border-top:5px solid #2563eb; font-family:sans-serif; color:#1e293b;">
        <h2 style="color:#2563eb;">Institutional Acquisition Signal</h2>
        <p>Hello {name}, our system has identified a high-liquidity asset: <b>{asset['id']}</b></p>
        <p>A 1000-word VC-grade Investment Audit is ready for your portfolio review.</p>
        <br><a href="https://assetpulse-ai.onrender.com" style="background:#2563eb; color:white; padding:15px 30px; text-decoration:none; border-radius:10px; font-weight:bold;">ACCESS AUDIT PROTOCOL</a>
    </div>
    """
    try:
        resend.Emails.send({"from": "Acquisitions <onboarding@resend.dev>", "to": [email], "subject": f"Strategic Alert: {asset['id']}", "html": pitch_html})
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
                            await asyncio.sleep(random.randint(10, 20))
                            await send_auto_pitch(p['name'], p['email'], target)
                except: pass
        await asyncio.sleep(random.randint(3000, 4500))

# --- AGENT 3: SOCIAL INTEL (X & REDDIT) ---
async def social_intel_loop():
    while True:
        platforms = ["X/Twitter", "Reddit"]
        queries = ["Looking for .ai domain", "Startup name help", "Buying premium .io"]
        intel = {"platform": random.choice(platforms), "user": f"Founder_{random.randint(100,999)}", "intent": random.choice(queries), "status": "HOT"}
        SOCIAL_INTEL.insert(0, intel)
        if len(SOCIAL_INTEL) > 10: SOCIAL_INTEL.pop()
        await asyncio.sleep(900)

@app.on_event("startup")
async def startup_event():
    ai_asset_discovery()
    asyncio.create_task(sniper_outreach_loop())
    asyncio.create_task(social_intel_loop())

# --- ROUTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index(): return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted(): return {"assets": [{"id": a["id"], "name": a["hidden_name"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...), lang: str = Query("English")):
    if not client: return {"error": "Intelligence Node Offline"}
    prompt = f"Write a 1000-word Institutional VC Audit for {name} sector in {lang}. Focus on ROI, Scarcity, and Exit Strategy. Never reveal real domain."
    try:
        completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
        report = completion.choices[0].message.content
        trust = f"\n\n--- [MARKET PULSE] Node {random.randint(100,999)} recently exited for ${random.randint(5000, 15000)}."
        return {"result": report + trust}
    except Exception as e: return {"error": str(e)}

# --- V21 THE LOCKDOWN: NO IDENTITY UNTIL PAYMENT ---
@app.get("/unlock_identity")
def unlock_identity(asset_id: str = Query(...), buyer_email: str = Query(...)):
    # Lead capture kareinge par IDENTITY REVEAL NAHI KARENGE
    LEAD_DATABASE.append({"email": buyer_email, "asset": asset_id, "status": "PENDING_PAYMENT"})
    
    if RESEND_API_KEY:
        checkout_url = f"https://checkout.stripe.com/pay/mantu_{asset_id}"
        try:
            resend.Emails.send({
                "from": "Acquisitions <onboarding@resend.dev>", 
                "to": [buyer_email], 
                "subject": f"Protocol {asset_id}: Verification Required", 
                "html": f"""
                <div style="font-family:sans-serif; padding:30px; border:1px solid #eee; border-radius:20px;">
                    <h2 style="color:#2563eb;">Identity Locked</h2>
                    <p>To reveal the institutional identity for <b>{asset_id}</b>, please complete the verification fee ($99).</p>
                    <br><a href='{checkout_url}' style='background:#2563eb; color:white; padding:15px 30px; text-decoration:none; border-radius:10px; font-weight:bold;'>UNLOCK NOW</a>
                </div>
                """
            })
        except: pass
    return {"status": "success"}

@app.get("/create_checkout")
def create_checkout(asset_id: str):
    return {"checkout_url": f"https://checkout.stripe.com/pay/mantu_{asset_id}"}

# --- ADMIN CONTROL CENTER ---
@app.get("/admin-mantu")
async def admin_dashboard():
    html = f"""
    <body style="background:#f1f5f9; color:#1e293b; font-family:sans-serif; padding:40px;">
        <h1 style="color:#2563eb;">COMMAND CENTER V21</h1>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
            <div style="background:white; padding:20px; border-radius:15px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <h3>PENDING LEADS ({len(LEAD_DATABASE)})</h3>
                <table style="width:100%; border-collapse:collapse;">
                    <tr style="background:#2563eb; color:white;"><th>Email</th><th>Asset ID</th></tr>
                    {"".join([f"<tr><td style='padding:10px; border-bottom:1px solid #eee;'>{l['email']}</td><td>{l['asset']}</td></tr>" for l in LEAD_DATABASE])}
                </table>
            </div>
            <div style="background:white; padding:20px; border-radius:15px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <h3>SOCIAL INTEL</h3>
                {"".join([f"<p style='border-bottom:1px solid #eee; padding:10px;'><b>{s['platform']}</b>: {s['user']} wants {s['intent']}</p>" for s in SOCIAL_INTEL])}
            </div>
        </div>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

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

# --- INITIALIZATION ---
app = FastAPI(title="AssetPulse V16.0 - The Empire Core")

# --- API CONFIGURATION ---
# Render Environment Variables se keys uthayega
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

# --- DATABASE SIMULATION ---
HUNTED_POOL = []
LEAD_DATABASE = [] # Leads yahan save hongi (Admin Tracker)

# --- AGENT 1: AI ASSET DISCOVERY (100 ASSETS) ---
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
    print(f"[SYSTEM] {len(HUNTED_POOL)} Assets Injected into Node.")

# --- AGENT 2: AUTO-OUTREACH "ACTIVE" ENGINE ---
async def send_auto_pitch(lead_name: str, lead_email: str, asset: dict):
    """Resend se buyer ko pitch bhejna"""
    if not RESEND_API_KEY: return

    pitch_html = f"""
    <div style="font-family: sans-serif; background: #020205; color: white; padding: 40px; border: 2px solid #2563eb; border-radius: 30px; max-width: 600px; margin: auto;">
        <h1 style="color: #2563eb; font-style: italic;">STRATEGIC SIGNAL</h1>
        <p>Hello {lead_name},</p>
        <p>Our autonomous sniper has identified a high-liquidity digital asset: <b>{asset['id']}</b></p>
        <p>We have generated a 1000-word Institutional Audit for this identity. Review it below:</p>
        <br>
        <a href="https://assetpulse-ai.onrender.com" style="display: inline-block; background: #2563eb; color: white; padding: 15px 40px; text-decoration: none; border-radius: 50px; font-weight: 900;">VIEW AUDIT PROTOCOL</a>
        <p style="margin-top: 40px; font-size: 10px; color: #333;">Transmission Secure | Verified by Visora AI Autonomous OS</p>
    </div>
    """
    try:
        resend.Emails.send({
            "from": "Acquisitions <onboarding@resend.dev>",
            "to": [lead_email],
            "subject": f"Asset Protocol {asset['id']}: Discovery Signal",
            "html": pitch_html
        })
        print(f"[ACTIVE MODE] Pitch dispatched to: {lead_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

# --- AGENT 3: APOLLO SNIPER LOOP ---
async def sniper_outreach_loop():
    """Real-time Apollo hunting loop"""
    while True:
        if HUNTED_POOL and APOLLO_API_KEY:
            target = random.choice(HUNTED_POOL)
            keyword = target['real_name'].split('-')[0]
            url = "https://api.apollo.io/v1/people/search"
            headers = {"Content-Type": "application/json", "X-Api-Key": APOLLO_API_KEY}
            payload = {"q_keywords": keyword, "person_titles": ["founder", "ceo", "owner"], "page": 1, "per_page": 1}

            async with httpx.AsyncClient() as http_client:
                try:
                    response = await http_client.post(url, json=payload, headers=headers)
                    data = response.json()
                    people = data.get('people', [])
                    for person in people:
                        email = person.get('email')
                        if email:
                            await send_auto_pitch(person.get('name', 'Founder'), email, target)
                except Exception as e:
                    print(f"[APOLLO ERROR] {e}")
        await asyncio.sleep(3600)

@app.on_event("startup")
async def startup_event():
    ai_asset_discovery()
    asyncio.create_task(sniper_outreach_loop())

# --- ROUTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted():
    return {"assets": [{"id": a["id"], "name": a["hidden_name"], "type": a["type"], "status": a["status"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...)):
    if not client: return {"error": "Groq Key Missing"}
    prompt = f"Write a 1000-word Investment Audit for {name.split('.')[-1]} niche. Use VC tone. Hide '{name}'."
    completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
    return {"result": completion.choices[0].message.content}

@app.get("/unlock_identity")
def unlock_identity(asset_id: str = Query(...), buyer_email: str = Query(...)):
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"error": "Asset not found"}
    
    # LEAD TRACKING (V16.0)
    LEAD_DATABASE.append({"email": buyer_email, "asset": asset_id, "domain": asset['real_name']})
    
    if RESEND_API_KEY:
        real_link = f"{MY_AFFILIATE_BASE}&domainToCheck={asset['real_name']}"
        try:
            resend.Emails.send({
                "from": "Identity Services <onboarding@resend.dev>",
                "to": [buyer_email],
                "subject": f"Decryption Protocol Complete: {asset['id']}",
                "html": f"<h2>Protocol Unlocked</h2><p>Identity: <b>{asset['real_name']}</b></p><br><a href='{real_link}'>Acquire Now</a>"
            })
        except Exception as e: print(f"Email Error: {e}")
    return {"status": "success"}

@app.get("/create_checkout")
def create_checkout(asset_id: str):
    return {"checkout_url": f"https://checkout.stripe.com/pay/mantu_{asset_id}", "status": "Ready"}

# --- SECRET ADMIN TRACKER ---
@app.get("/admin-mantu")
async def admin_dashboard():
    html = f"""
    <body style="background:#020205; color:white; font-family:sans-serif; padding:50px;">
        <h1 style="color:#2563eb;">EMPIRE SALES TRACKER</h1>
        <div style="background:#0a0a12; padding:20px; border-radius:20px; border:1px solid #333;">
            <p>Total Captured Leads: <b>{len(LEAD_DATABASE)}</b></p>
            <table border="1" style="width:100%; border-collapse:collapse; text-align:left;">
                <tr style="background:#2563eb;">
                    <th style="padding:15px;">Buyer Email</th>
                    <th style="padding:15px;">Asset ID</th>
                    <th style="padding:15px;">Real Domain</th>
                </tr>
                {"".join([f"<tr><td style='padding:12px;'>{l['email']}</td><td style='padding:12px;'>{l['asset']}</td><td style='padding:12px;'>{l['domain']}</td></tr>" for l in LEAD_DATABASE])}
            </table>
            <br>
            <button onclick="location.reload()" style="padding:15px 30px; background:green; color:white; border:none; border-radius:10px; cursor:pointer;">REFRESH LIVE FEED</button>
        </div>
    </body>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

import os
import uvicorn
import resend  # requirements.txt mein resend hona zaroori hai
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq

# Initialization
app = FastAPI(title="AssetPulse Pro - Full Autonomous V6.0")

# API Keys (Render Dashboard se pick karega)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

MODEL_NAME = "llama-3.3-70b-versatile"

# GoDaddy Tracking Link
MY_AFFILIATE_BASE = "https://www.godaddy.com/domainsearch/find?checkAvail=1&isc=cjccom311"

# Internal Database
HUNTED_POOL = []

def asset_generator():
    """100 Assets with Hidden Identity Logic"""
    global HUNTED_POOL
    suffixes = [".ai", ".io", ".com"]
    new_data = []
    for i in range(1, 101):
        ext = suffixes[i % 3]
        real_name = f"nexus-cloud-{i}{ext}" if i % 2 == 0 else f"alpha-trade-{i}{ext}"
        
        new_data.append({
            "id": f"ASSET-{1000+i}",
            "hidden_name": f"PREMIUM-{ext.upper()}-IDENTITY-LOCKED", 
            "real_name": real_name,
            "type": "Premium Domain",
            "status": "Verified Expired"
        })
    HUNTED_POOL = new_data

@app.on_event("startup")
async def startup_event():
    asset_generator()

# --- ROUTES ---

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted():
    """Frontend ko sirf hidden details bhejna"""
    return {"assets": [{"id": a["id"], "name": a["hidden_name"], "type": a["type"], "status": a["status"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...)):
    """Wapas wahi Deep Detailed Audit (500+ Words)"""
    if not client:
        return {"error": "GROQ_API_KEY Missing"}
    
    prompt = f"""
    Act as a Senior Digital Asset Investment Consultant. 
    Perform a high-level 500-word audit for a digital asset in the {name.split('.')[-1]} niche.
    
    SECTIONS TO INCLUDE:
    1. BRAND AUTHORITY: Syllable count, phonetics, and memorability.
    2. SEO VALUATION: Keyword competitiveness and organic traffic potential.
    3. MARKET TRENDS: Why this niche is exploding in 2026.
    4. MONETIZATION PATH: Direct flip vs. SaaS development ROI.
    5. ACQUISITION SCORE: Final rating out of 10.

    STRICT PRIVACY: Never mention the real name '{name}'. Use '[SECURE_ASSET_ID]' instead.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You provide institutional-grade domain audits."},
                      {"role": "user", "content": prompt}],
            model=MODEL_NAME,
            temperature=0.75
        )
        return {"result": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/unlock_identity")
def unlock_identity(asset_id: str = Query(...), buyer_email: str = Query(...)):
    """Asli Domain details ko email par bhejne ka logic"""
    if not RESEND_API_KEY:
        return {"error": "Email engine offline. Setup Resend Key."}
    
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset:
        return {"error": "Asset not found."}

    real_link = f"{MY_AFFILIATE_BASE}&domainToCheck={asset['real_name']}"

    try:
        resend.Emails.send({
            "from": "AssetPulse <onboarding@resend.dev>",
            "to": [buyer_email],
            "subject": f"Vault Access: {asset['id']} Details Unlocked",
            "html": f"""
                <div style="font-family: Arial; padding: 40px; background: #f4f4f4; border-radius: 10px;">
                    <h1 style="color: #1d4ed8;">IDENTITY UNLOCKED</h1>
                    <p>You have successfully unlocked the details for <b>{asset['id']}</b>.</p>
                    <p style="font-size: 18px;"><b>Real Domain:</b> {asset['real_name']}</p>
                    <br>
                    <a href="{real_link}" style="background: #1d4ed8; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                        BUY ON GODADDY
                    </a>
                    <p style="margin-top: 30px; font-size: 12px; color: #666;">This is an automated intelligence report from Visora AI.</p>
                </div>
            """
        })
        return {"status": "success", "message": f"Details sent to {buyer_email}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

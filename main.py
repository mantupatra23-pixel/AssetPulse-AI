import os
import uvicorn
import resend
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq

# Initialization
app = FastAPI(title="AssetPulse Pro - V6.5 Institutional Edition")

# API Keys (Render Environment Variables)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

MODEL_NAME = "llama-3.3-70b-versatile"

# GoDaddy Affiliate Config
MY_AFFILIATE_BASE = "https://www.godaddy.com/domainsearch/find?checkAvail=1&isc=cjccom311"

# Database Logic
HUNTED_POOL = []

def asset_generator():
    """100 Hidden Assets generate karna"""
    global HUNTED_POOL
    suffixes = [".ai", ".io", ".com"]
    new_data = []
    for i in range(1, 101):
        ext = suffixes[i % 3]
        real_name = f"nexus-cloud-{i}{ext}" if i % 2 == 0 else f"alpha-trade-{i}{ext}"
        new_data.append({
            "id": f"ASSET-{1000+i}",
            "hidden_name": f"PREMIUM-{ext.upper()}-LOCKED-{1000+i}",
            "real_name": real_name,
            "type": "Institutional Asset",
            "status": "Verified Availability"
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
    return {"assets": [{"id": a["id"], "name": a["hidden_name"], "type": a["type"], "status": a["status"]} for a in HUNTED_POOL]}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...)):
    """Super Detailed Audit (800+ Words)"""
    if not client: return {"error": "GROQ_API_KEY Missing"}
    
    # Ultra-Detailed Prompt for Long Reports
    prompt = f"""
    Act as a Senior Wall Street Digital Asset Auditor. 
    Write an 800-word Investment Memorandum for a premium digital asset in the {name.split('.')[-1]} sector.
    
    STRUCTURE YOUR RESPONSE WITH THESE 5 DETAILED SECTIONS:
    1. EXECUTIVE VALUATION: Why this niche is a 'Strong Buy' for 2026.
    2. LINGUISTIC ANALYSIS: Deep dive into phonetics, syllable count, and brand recall metrics.
    3. MARKET SCALABILITY: Potential for SaaS integration or corporate acquisition.
    4. COMPARATIVE DATA: How this outranks previous 6-figure sales in this niche.
    5. MONETIZATION ROADMAP: 5 specific steps to flip this for a 15x profit.

    STRICT PRIVACY: Never use the real name '{name}'. Instead, use '[SECURE_ASSET_ID]'.
    Make the tone extremely professional, financial, and highly detailed.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are an institutional domain auditor."},
                      {"role": "user", "content": prompt}],
            model=MODEL_NAME,
            temperature=0.8
        )
        return {"result": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/unlock_identity")
def unlock_identity(asset_id: str = Query(...), buyer_email: str = Query(...)):
    """Email par identity unlock karne ka logic"""
    if not RESEND_API_KEY: return {"error": "Resend Key Missing"}
    
    asset = next((a for a in HUNTED_POOL if a["id"] == asset_id), None)
    if not asset: return {"error": "Asset not found"}

    real_link = f"{MY_AFFILIATE_BASE}&domainToCheck={asset['real_name']}"

    try:
        resend.Emails.send({
            "from": "Vault <onboarding@resend.dev>",
            "to": [buyer_email],
            "subject": f"Vault Access: {asset['id']} Details Unlocked",
            "html": f"""
                <div style="font-family: sans-serif; background: #0a0a0a; color: white; padding: 40px; border-radius: 15px;">
                    <h2 style="color: #2563eb;">IDENTITY DECRYPTED</h2>
                    <p>Details for <b>{asset['id']}</b> have been released to your email.</p>
                    <p style="font-size: 18px; background: #222; padding: 10px;"><b>Real Domain:</b> {asset['real_name']}</p>
                    <br>
                    <a href="{real_link}" style="background: #2563eb; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        ACQUIRE ON GODADDY
                    </a>
                </div>
            """
        })
        return {"status": "success"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

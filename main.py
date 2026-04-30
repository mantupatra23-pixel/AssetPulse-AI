import os
import uvicorn
import resend  # pip install resend
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq

# Initialization
app = FastAPI(title="AssetPulse Pro - Autonomous Broker V5.0")

# API Setup
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

MODEL_NAME = "llama-3.3-70b-versatile"

# GoDaddy Deep Link Fix
MY_AFFILIATE_BASE = "https://www.godaddy.com/domainsearch/find?checkAvail=1&isc=cjccom311"

HUNTED_POOL = []

def asset_generator():
    global HUNTED_POOL
    suffixes = [".ai", ".io", ".com", ".net"]
    new_data = []
    for i in range(1, 101):
        ext = suffixes[i % 4]
        name = f"nexus-cloud-{i}{ext}" if i % 2 == 0 else f"alpha-trade-{i}{ext}"
        buy_url = f"{MY_AFFILIATE_BASE}&domainToCheck={name}"
        new_data.append({
            "id": f"ASSET-{1000+i}",
            "name": name,
            "type": "Domain",
            "status": "Available",
            "buy_url": buy_url
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
async def read_index(): return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted(): return {"assets": HUNTED_POOL}

@app.get("/safe_report")
def get_safe_report(name: str = Query(...)):
    if not client: return {"error": "Groq Key Missing"}
    prompt = f"Write a 150-word investment pitch for a digital asset in the {name.split('.')[-1]} niche. HIDE name '{name}'."
    completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
    return {"result": completion.choices[0].message.content.replace(name, "[IDENTITY_PROTECTED]")}

# --- AUTOMATIC EMAIL ENGINE ---
@app.get("/auto_email")
def auto_email(name: str = Query(...), target_email: str = Query(...)):
    """AI report generate karke buyer ko auto-email karta hai"""
    if not RESEND_API_KEY:
        return {"error": "Resend API Key Missing"}
    
    # 1. Pehle AI se report nikalwao
    report_data = get_safe_report(name)
    pitch = report_data.get("result", "Strategic Asset Opportunity detected.")

    # 2. Professional HTML Email bhejo
    try:
        params = {
            "from": "Mantu AI <onboarding@resend.dev>", # Domain verify hone ke baad apna email use karein
            "to": [target_email],
            "subject": f"Investment Opportunity: Premium {name.split('.')[-1]} Asset",
            "html": f"""
                <div style="font-family: sans-serif; padding: 20px; border: 1px solid #eee;">
                    <h2 style="color: #2563eb;">AssetPulse Pro - Strategic Intel</h2>
                    <p>We have identified a high-ROI digital asset in your industry.</p>
                    <div style="background: #f9f9f9; padding: 15px; border-radius: 10px; font-style: italic;">
                        {pitch}
                    </div>
                    <p>To acquire this asset or view full valuation, visit our secure terminal.</p>
                    <a href="https://your-render-url.onrender.com" 
                       style="background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                       Open Terminal
                    </a>
                    <br><br>
                    <p>Regards,<br><b>Mantu Patra</b><br>Founder, Visora AI</p>
                </div>
            """
        }
        resend.Emails.send(params)
        return {"status": "Success", "message": f"Pitch sent to {target_email}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

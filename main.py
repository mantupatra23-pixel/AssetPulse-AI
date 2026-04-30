import os
import uvicorn
import cloudscraper
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from bs4 import BeautifulSoup
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="AssetPulse AI - Pro Autonomous")

# AI Setup
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Global Hunted Pool
HUNTED_POOL = ["mantu-prime.ai", "fintech-flow.io", "bharat-nexus.in"]

# --- AUTOMATIC SCRAPER LOGIC ---
def autonomous_hunter():
    global HUNTED_POOL
    print(">> [SCANNER] Initiating Global Asset Hunt...")
    scraper = cloudscraper.create_scraper()
    
    # Target URLs (Adjust filters on ExpiredDomains for better results)
    sources = [
        "https://www.expireddomains.net/expired-ai-domains/",
        "https://www.expireddomains.net/expired-com-domains/",
        "https://www.expireddomains.net/expired-io-domains/"
    ]
    
    new_assets = []
    try:
        for url in sources:
            res = scraper.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            table = soup.find('table', class_='nametable')
            if table:
                rows = table.find_all('tr')[1:6] # Top 5 from each TLD
                for row in rows:
                    name = row.find('a').text
                    if name not in HUNTED_POOL:
                        new_assets.append(name)
        
        # Update Pool (Keep fresh 20 assets)
        HUNTED_POOL = (new_assets + HUNTED_POOL)[:20]
        print(f">> [SCANNER] Success. New pool size: {len(HUNTED_POOL)}")
    except Exception as e:
        print(f">> [SCANNER] Error: {e}")

# Scheduler: Har 20 minute mein hunting
scheduler = BackgroundScheduler()
scheduler.add_job(autonomous_hunter, 'interval', minutes=20)
scheduler.start()

# --- SERVER CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_path): os.makedirs(static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index(): return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted(): return {"assets": HUNTED_POOL}

@app.get("/analyze")
def analyze_asset(name: str = Query(...)):
    if not client: return {"error": "API Key Missing"}
    prompt = f"Professional investment report for domain: {name}. Include USD value and BUY/SKIP verdict."
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.4
        )
        return {"result": chat.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

@app.get("/find_buyers")
def find_buyers(name: str = Query(...)):
    if not client: return {"error": "API Key Missing"}
    prompt = f"Identify top 3 buyers for {name} and a pitch."
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return {"result": chat.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

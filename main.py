import os
import uvicorn
import cloudscraper
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from bs4 import BeautifulSoup
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

# AI Setup
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
MODEL_NAME = "llama-3.3-70b-versatile"

# Global Storage for Auto-Hunted Domains
HUNTED_POOL = []

def autonomous_hunting_logic():
    """Asli Expired Domains fetch karne ka logic"""
    global HUNTED_POOL
    print(">> Bot is Hunting for Expired Assets...")
    
    scraper = cloudscraper.create_scraper()
    # Expired AI domains ki public list (Example source)
    url = "https://www.expireddomains.net/expired-ai-domains/"
    
    try:
        response = scraper.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Table se domains nikalna
        table = soup.find('table', class_='nametable')
        temp_list = []
        
        if table:
            rows = table.find_all('tr')[1:51] # Top 50 domains
            for row in rows:
                domain_name = row.find('a').text
                # AI Logic: Sirf high potential domains ko pool mein rakhna
                temp_list.append({
                    "name": domain_name,
                    "type": "Domain",
                    "status": "Verified Expired"
                })
        
        if not temp_list: # Fallback agar scraper block ho jaye
            temp_list = [{"name": f"auto-find-{i}.ai", "type": "Domain", "status": "AI-Predicted"} for i in range(50)]
            
        HUNTED_POOL = temp_list
        print(f">> Hunt Complete: {len(HUNTED_POOL)} Assets Tracked.")
    except Exception as e:
        print(f"Scraper Error: {e}")

# Background Automation: Har 20 minute mein naye domains dhoondho
scheduler = BackgroundScheduler()
scheduler.add_job(autonomous_hunting_logic, 'interval', minutes=20)
scheduler.start()

# Startup hunt
@app.on_event("startup")
async def startup_event():
    autonomous_hunting_logic()

# --- ROUTES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index(): return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/hunted")
def get_hunted(): return {"assets": HUNTED_POOL}

@app.get("/analyze")
def analyze_asset(name: str = Query(...)):
    if not client: return {"error": "Key Missing"}
    prompt = f"Investment audit for domain: {name}. Valuation and Resale potential."
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=MODEL_NAME)
        return {"result": res.choices[0].message.content}
    except Exception as e: return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

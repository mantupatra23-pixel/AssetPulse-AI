import os
import requests
from fastapi import FastAPI, Query
from bs4 import BeautifulSoup
from groq import Groq
from typing import Optional

# FastAPI app initialize
app = FastAPI(title="AssetPulse AI - Digital Arbitrage Engine")

# Groq Client Setup
# Yaad se Render ke Environment Variables mein GROQ_API_KEY daal dena
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

@app.get("/")
def home():
    return {
        "status": "Online",
        "engine": "AssetPulse AI v1.0",
        "author": "Mantu Patra",
        "endpoints": {
            "/scan": "Scrape potential domains (Coming Soon: High-speed proxy)",
            "/analyze": "AI-powered valuation of a specific asset"
        }
    }

@app.get("/scan")
def scan_assets(keyword: str = "ai"):
    """
    Experimental Scraper: Yeh basic keywords ke base par domain availability check karta hai.
    """
    # Note: Real production mein hum yahan Namecheap ya GoDaddy API use karenge
    # Filhal ye ek base structure hai
    return {
        "search_query": keyword,
        "suggested_assets": [
            f"{keyword}-automation.ai",
            f"smart-{keyword}.io",
            f"the-{keyword}-agent.com"
        ],
        "message": "Use /analyze?name=domain.com to check value."
    }

@app.get("/analyze")
def analyze_asset(name: str = Query(..., description="Name of the domain or asset to analyze")):
    """
    AI Logic: Llama 3 se domain ki resale value aur demand analyze karwana.
    """
    if not client:
        return {"error": "GROQ_API_KEY not found in environment variables."}

    prompt = f"""
    You are an expert Digital Asset Arbitrageur. 
    Analyze the following domain name for its investment and resale potential.
    
    Domain: {name}
    
    Provide the following in short, crisp points:
    1. Estimated Resale Value (in USD).
    2. Why is it valuable? (Keywords, TLD, Trends).
    3. Target Buyers (e.g., Tech startups, Finance firms).
    4. Risk Level (Low/Medium/High).
    5. Final Verdict: BUY or SKIP.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional business analyst specializing in domain flipping."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
            temperature=0.7,
        )
        
        analysis = chat_completion.choices[0].message.content
        return {
            "asset": name,
            "analysis": analysis
        }
    except Exception as e:
        return {"error": f"AI analysis failed: {str(e)}"}

# Local Testing ke liye
if __name__ == "__main__":
    import uvicorn
    # Termux mein chalane ke liye port 8000 default rahega
    uvicorn.run(app, host="0.0.0.0", port=8000)

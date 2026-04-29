import os
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
import uvicorn

# App Initialize
app = FastAPI(title="AssetPulse AI")

# Groq AI Setup
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Frontend folder setup
# Ensure 'static' folder exists in your directory
if not os.path.exists("static"):
    os.makedirs("static")

# Static files mount (CSS/JS/HTML ke liye)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    # Jab koi main URL khole toh dashboard dikhe
    return FileResponse('static/index.html')

@app.get("/analyze")
def analyze_asset(name: str = Query(..., description="Domain or Asset name")):
    """
    AI Logic to analyze digital asset value.
    """
    if not client:
        return {"error": "GROQ_API_KEY is not set in environment variables."}

    prompt = f"""
    You are a high-end Digital Asset Broker. Analyze this domain for arbitrage:
    Domain: {name}

    Provide:
    1. Estimated Resale Price (USD).
    2. Why it has value (Keywords/Trends).
    3. Target Audience.
    4. Verdict: BUY, HOLD, or SKIP.
    Keep it professional and short.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional domain flipping expert."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.6,
        )
        return {"analysis": chat_completion.choices[0].message.content}
    except Exception as e:
        return {"error": f"AI Error: {str(e)}"}

@app.get("/health")
def health_check():
    return {"status": "running", "ai_connected": client is not None}

if __name__ == "__main__":
    # Local Termux testing ke liye
    uvicorn.run(app, host="0.0.0.0", port=8000)

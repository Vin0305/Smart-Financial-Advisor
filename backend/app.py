import sys
import os

# Add the backend folder to Python path BEFORE any imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now it's safe to import from utils
from utils import analyze_trends

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import google.generativeai as genai
from fastapi import HTTPException
# import requests

load_dotenv()
app = FastAPI()

# Initialize 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_advice(prompt):
    # model = genai.GenerativeModel("gemini-pro")
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating advice: {str(e)}"
    
    
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Smart Financial Advisor API is running."}

@app.get("/analyze")
def get_advice(file: str = "data/sample_spending.csv"):
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        current_model = genai.GenerativeModel("gemini-1.5-flash")
        
        #trends_text = analyze_trends("data/sample_spending.csv")
        print(f"Analyzing file: {file}")
        
        result = analyze_trends(file)
        trends_text = result["trends"]
        forecasts = result["forecasts"]
        
        print("Trends:", trends_text)
        print("Forecasts:", forecasts)

        prompt = f"""You are a helpful financial advisor. Based on these user spending trends:
    {trends_text}
    
    Forecasts for next month:
    {format_forecast(forecasts)}

    Give 2-3 simple, personalized, jargon-free financial tips to help the user save money."""
        
        response = current_model.generate_content(prompt)   
        # advice = get_gemini_advice(prompt)
        advice = response.text
        print("Advice received from Gemini:", advice)
        return {
            "advice": advice,
            "trends": trends_text,
            "forecasts": forecasts
            }

    except Exception as e:
        print("Error in /analyze:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
def format_forecast(forecasts):
    lines = [f"{k}: ${v:.2f}" for k, v in forecasts.items()]
    return "\n".join(lines)
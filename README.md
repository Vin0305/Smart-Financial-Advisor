# Smart Financial Advisor Using LLMs & Spending Patterns

 An AI-powered financial advisor that reads spending habits and gives personalized, jargon-free advice using Google Gemini API.  
Detects trends, forecasts budgets, and helps users make smarter money decisions.

---

##  Project Description

The **Smart Financial Advisor** is a full-stack personal finance tool that uses large language models (LLMs) to analyze spending patterns and provide actionable advice.

Built with:
- FastAPI (backend)
- Streamlit (frontend)
- Google Gemini 1.5 Flash (for natural language financial advice)
- Pandas + Scikit-learn (for data analysis and forecasting)
- Local CSV upload support

This project is perfect for developers learning:
- Full-stack web development
- LLM integration
- Data visualization
- Budget forecasting
- Trend detection

---

##  Features

| Feature | Description |
|--------|-------------|
| 📊 Trend Detection | Analyzes spending categories over time and detects increases or decreases |
| 💬 Personalized Advice | Uses Google Gemini API to generate clear, easy-to-understand tips |
| 🔮 Budget Forecasting | Predicts next month’s spending using linear regression |
| 📤 CSV Upload Support | Allows users to upload their own spending history (via Streamlit) |
| 📈 Chart Visualization | Shows monthly spending trends in charts |
| 🎯 Goal-Based Planning | Suggests cuts per category to meet savings goals |
| 📝 Explainable Insights | Shows exact spending trends that triggered each piece of advice |
| 📁 Save Past Analyses | Stores past results so users can compare over time |
| 📄 PDF Export | Lets users download their financial advice as a PDF |

---

##  Tech Stack

| Layer | Technology |
|------|------------|
| Backend | FastAPI |
| Frontend | Streamlit |
| LLM | Google Gemini 1.5 Flash |
| Data Analysis | Pandas, NumPy, Scikit-Learn |
| UI Charts | Matplotlib |
| File Storage | CSV |
| PDF Reports | fpdf2 |
| Environment | python-dotenv |
| Deployment Ready | Yes (can be containerized or deployed on Vercel / Railway)

---

##  Folder Structure

Smart_Fin_Advisor/

│

├── backend/ # FastAPI logic

│ ├── app.py # Main backend API

│ └── utils.py # Spending trend analysis functions

│

├── dashboard/ # Streamlit frontend

│ └── app.py # Dashboard with visualizations and user input

│

├── data/ # CSV files

│ ├── sample_spending.csv

│ └── uploaded_spending.csv # Auto-created when user uploads a file

│

├── .env # Holds Gemini API key

├── .gitignore # Prevents sensitive files from being pushed

├── LICENSE # MIT License (from GitHub)

└── README.md # This file!


---

##  Requirements

Make sure you install all dependencies:
pip install fastapi uvicorn streamlit pandas numpy scikit-learn google-generativeai fpdf2 python-dotenv

Sample .env file: GEMINI_API_KEY=your_gemini_api_key_here

---
## Running the App

Step 1: Start the backend

        cd your/path/to project folder/backend
        uvicorn app:app --reload

Step 2: Open another terminal and start the frontend

        cd your/path/to project folder/dashboard
        streamlit run app.py

Step 3: Go to: http://localhost:8501

        Click " Analyze My Spending" to get AI-generated advice based on your spending CSV.

---
## How to use it
Upload a spending CSV via the UI (optional)

Click " Analyze My Spending"

View:

     Spending trends
     
     Forecasted amounts

     Goal-based suggestions
    
     Visual charts

     Downloadable PDF report

     Sample CSV: trial.csv(can use your own. Make sure there are more than 2 entries per category across at least 2 months; Use YYYY-MM-DD or DD-MM-YYYY date formats only.)

## Reference Images
For visual setup and UI examples, please refer to the included images in the `images/` folder. These help explain how the app works and what the interface looks like.


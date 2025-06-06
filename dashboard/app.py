import streamlit as st
import requests
import pandas as pd
import os
import json
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Financial Advisor", layout="centered")
st.title(" Smart Financial Advisor")
st.write("Get personalized financial advice based on your spending trends.")

uploaded_file = st.file_uploader("Upload your spending CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.to_csv("data/uploaded_spending.csv", index=False)
    st.success("File uploaded successfully!")
    
file_to_use = "data/uploaded_spending.csv" if os.path.exists("data/uploaded_spending.csv") else "data/sample_spending.csv"

# load current data
df = pd.read_csv(file_to_use)
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
df = df.dropna(subset=['Date'])
df['Month'] = df['Date'].dt.to_period('M').astype(str)

# Goal Input
goal = st.number_input("Enter your savings goal for next month:", min_value=0)

if st.button(" Analyze My Spending"):
    try:
        with st.spinner("Analyzing your spending..."):
            # res = requests.get("http://127.0.0.1:8000/analyze")
            res = requests.get(f"http://127.0.0.1:8000/analyze?file={file_to_use}")
            if res.status_code == 200:
                result = res.json()
                advice = res.json().get("advice", "No advice available.")
                trends = result.get("trends", "")
                forecasts = result.get("forecasts", {})
                
                st.success("Here’s your advice:")
                st.markdown(f"> {advice}")
                
                #show forecasts
                st.subheader("Monthly Forecasts")
                for category, amount in forecasts.items():
                    st.write(f"- **{category}**: ${amount:.2f}")
                    
                # Goal Planning
                if goal > 0:
                    total_spend = df['Amount'].sum()
                    cut_needed = total_spend - goal
                    current_avg = df.groupby('Category')['Amount'].mean()
                    cuts = (current_avg / total_spend) * cut_needed

                    st.subheader(" Goal-Based Suggestions")
                    for category, amount in cuts.items():
                        st.write(f"- Try reducing **{category}** by ${amount:.2f} next month.")

                # Chart
                st.subheader(" Monthly Spending Trends")
                fig, ax = plt.subplots()
                df.groupby(['Month', 'Category'])['Amount'].sum().unstack().plot(kind='line', ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)

                # Save Analysis
                record = {
                    "timestamp": str(datetime.now()),
                    "trends": trends,
                    "forecasts": forecasts,
                    "advice": advice
                }
                with open("analysis_history.json", "a") as f:
                    f.write(json.dumps(record) + "\n")

            else:
                st.error(f"Backend returned status code: {res.status_code}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
        
#pdf export
def export_to_pdf(advice_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Smart Financial Advisor Report", ln=True, align='C')
    pdf.multi_cell(0, 10, txt=advice_text)
    pdf.output("financial_advice.pdf")
    return "financial_advice.pdf"

# st.markdown(f"> {advice}")

if 'advice' in locals() or 'advice' in globals():
    if st.button(" Export Advice as PDF"):
        pdf_path = export_to_pdf(advice)
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="financial_advice.pdf")

# View Past Analyses
if st.checkbox(" View Past Analysis"):
    try:
        with open("analysis_history.json", "r") as f:
            analyses = [json.loads(line) for line in f.readlines()]
        selected = st.selectbox("Select a past analysis", analyses, format_func=lambda x: x["timestamp"])
        st.write("Trends:")
        st.markdown(selected["trends"])
        st.write("Forecasts:")
        st.json(selected["forecasts"])
        st.write("Advice:")
        st.markdown(selected["advice"])
    except FileNotFoundError:
        st.warning("No past analysis found.")
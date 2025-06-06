import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def analyze_trends(file_path):
    df = pd.read_csv(file_path)
    print("Columns found:", df.columns.tolist())
    df.columns = df.columns.str.strip()  # Strip any spaces from headers
    print("Columns after strip:", df.columns.tolist())
    
    if 'Category' not in df.columns:
        raise ValueError("Column 'Category' is missing after reading the file.")
    
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    df = df.dropna(subset=['Date'])
    # df = pd.read_csv(csv_path, parse_dates=['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    monthly = df.groupby(['Month', 'Category'])['Amount'].sum().reset_index()

    trends = []
    forecasts = {}
    
    for category in monthly['Category'].unique():
        cat_data = monthly[monthly['Category'] == category]
        if len(cat_data) >= 2:
            diff = cat_data['Amount'].iloc[-1] - cat_data['Amount'].iloc[-2]
            trend = "increased" if diff > 0 else "decreased"
            percent = abs(diff) / cat_data['Amount'].iloc[-2] * 100
            trends.append(f"{category} spending has {trend} by {percent:.2f}% last month.")
            
            # forecast next month
            forecasts[category] = forecast_category(df[df['Category'] == category], category)
    
    # return "\n".join(trends) or "Not enough data to detect trends."
    return {
        "trends": "\n".join(trends) or "Not enough data to detect trends.",
        "forecasts": forecasts,
        "df": df
    }

def forecast_category(df, category):
    cat_data = df[df['Category'] == category].copy()
    if len(cat_data) < 2:
        return None

    # Ensure numeric amounts
    cat_data = cat_data[pd.to_numeric(cat_data['Amount'], errors='coerce').notnull()]
    if len(cat_data) < 2:
        return None
    
    cat_data['Month_Num'] = np.arange(len(cat_data))
    X = cat_data[['Month_Num']]
    y = cat_data['Amount'].astype(float)

    try:
        model = LinearRegression()
        model.fit(X, y)

        next_month = len(cat_data)
        prediction = model.predict([[next_month]])
        return round(prediction[0], 2)
    
    except Exception as e:
        print(f"Error forecasting {category}: {e}")
        return None
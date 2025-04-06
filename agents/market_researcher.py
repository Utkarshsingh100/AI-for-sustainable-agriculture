import ollama
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'data', 'market_researcher_dataset.csv'))

def get_market_insights(user_input):
    try:
        df = pd.read_csv(DATA_PATH)

        summary = df.groupby('Product').agg({
            'Market_Price_per_ton': 'mean',
            'Demand_Index': 'mean',
            'Supply_Index': 'mean',
            'Consumer_Trend_Index': 'mean'
        }).reset_index()

        summary['Market_Score'] = (
            summary['Market_Price_per_ton'] * 0.3 +
            summary['Demand_Index'] * 0.3 +
            summary['Consumer_Trend_Index'] * 0.3 -
            summary['Supply_Index'] * 0.1
        )

        summary = summary.sort_values('Market_Score', ascending=False)
        top_crop = summary.iloc[0]['Product']

        table = summary.head(5).to_string(index=False)

        prompt = f"""
You are an agricultural market analyst. Recommend the best crop(s) to sell next month based on this market data.

SUMMARY TABLE:
{table}

QUESTION:
{user_input}

Limit response to the top 1–2 crops. Be direct, use data points if needed, and keep it under 3 sentences.
"""

        response = ollama.chat(
            model='phi',
            messages=[
                {'role': 'system', 'content': 'You are a concise agricultural market analyst. No fluff. Just actionable insights.'},
                {'role': 'user', 'content': prompt}
            ]
        )

        return response['message']['content'].strip()

    except Exception as e:
        return f"❌ Error while analyzing market data: {e}"

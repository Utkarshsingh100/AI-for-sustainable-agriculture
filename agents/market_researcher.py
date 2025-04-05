import ollama
import pandas as pd

DATA_PATH = 'data/market_researcher_dataset.csv'


def get_market_insights(user_input):
    try:
        df = pd.read_csv(DATA_PATH)

        # Group by Product to get average price, demand, and trend scores
        summary = df.groupby('Product').agg({
            'Market_Price_per_ton': 'mean',
            'Demand_Index': 'mean',
            'Supply_Index': 'mean',
            'Consumer_Trend_Index': 'mean'
        }).reset_index()

        # Sort by high demand and low supply (higher score = better market potential)
        summary['Market_Score'] = (
            summary['Market_Price_per_ton'] * 0.3 +
            summary['Demand_Index'] * 0.3 +
            summary['Consumer_Trend_Index'] * 0.3 -
            summary['Supply_Index'] * 0.1
        )

        top_crop = summary.sort_values('Market_Score', ascending=False).iloc[0]['Product']

        # Send summary data and top crop to the model
        table = summary.to_string(index=False)

        prompt = f"""
You are an agriculture market analyst helping a farmer choose the most profitable crop for next month.

Here is a market summary table with averaged metrics for each crop:
{table}

Based on the current data and trends, answer the following question:

QUESTION:
{user_input}

Answer clearly and recommend the best crop to sell next month based on demand, price, and consumer trend index.
"""

        response = ollama.chat(
            model='phi',
            messages=[
                {'role': 'system', 'content': 'You are a data-driven agricultural market analyst.'},
                {'role': 'user', 'content': prompt}
            ]
        )
        return response['message']['content']

    except Exception as e:
        return f"❌ Error while analyzing market data: {e}"

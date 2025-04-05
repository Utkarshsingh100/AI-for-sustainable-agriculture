# agents/weather_station.py

import ollama
import pandas as pd

DATA_PATH = 'data/farmer_advisor_dataset.csv'  # or you can use a separate weather dataset if available

def get_weather_info(user_input):
    try:
        # You can include relevant data if needed; here we simulate weather context
        df = pd.read_csv(DATA_PATH)
        top_rows = df.head(5).to_string(index=False)

        prompt = f"""
You are a weather analysis assistant for farmers. Help assess how current or upcoming weather events might impact farming activities like planting, irrigation, or harvesting.

Example weather data:
{top_rows}

QUESTION:
{user_input}
"""

        response = ollama.chat(
            model='phi',
            messages=[
                {"role": "system", "content": "You are a smart assistant that helps farmers plan around weather."},
                {"role": "user", "content": prompt}
            ]
        )

        return response['message']['content']

    except Exception as e:
        return f"❌ Error while processing weather info: {e}"

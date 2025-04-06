import os
import ollama
import pandas as pd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'data', 'farmer_advisor_dataset.csv'))


def get_weather_info(user_input):
    try:
  
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

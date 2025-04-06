import os
import ollama
import pandas as pd
from agents.multi_agent_router import ask_agent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'data', 'farmer_advisor_dataset.csv'))

def get_advice(user_input):
    try:
        df = pd.read_csv(DATA_PATH)
        top_rows = df.head(5).to_string(index=False)

        collaborative_note = ""
        if any(keyword in user_input.lower() for keyword in ['sell', 'price', 'profit', 'market']):
            print("🔁 Collaborating with Market Researcher...")
            market_insights = ask_agent("market_researcher", user_input)
            collaborative_note = f"\n\n[Market Researcher says: {market_insights.strip()}]"

        elif any(keyword in user_input.lower() for keyword in ['rain', 'temperature', 'weather', 'irrigation']):
            print("🔁 Collaborating with Weather Station...")
            weather_insights = ask_agent("weather_station", user_input)
            collaborative_note = f"\n\n[Weather Station says: {weather_insights.strip()}]"

        prompt = f"""
You are a farming advisor who provides precise, sustainable, and resource-optimized suggestions to farmers.
Use the following data and any additional insights to suggest what crop a farmer should grow.

DATA SAMPLE:
{top_rows}

QUESTION:
{user_input}
{collaborative_note}

Be brief. Give only the most relevant advice in 2–3 sentences.
"""

        response = ollama.chat(
            model='phi',
            messages=[
                {'role': 'system', 'content': 'You are a concise and smart farming advisor. Avoid filler words and get straight to the point.'},
                {'role': 'user', 'content': prompt}
            ]
        )

        return response['message']['content'].strip()

    except Exception as e:
        return f"Error while processing advice: {e}"

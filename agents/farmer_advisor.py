# agents/farmer_advisor.py

import ollama
import pandas as pd
from agents.multi_agent_router import ask_agent

DATA_PATH = 'data/farmer_advisor_dataset.csv'

def get_advice(user_input):
    try:
        df = pd.read_csv(DATA_PATH)
        top_rows = df.head(5).to_string(index=False)

        # If the user input is related to profit/sales/market, collaborate
        if any(keyword in user_input.lower() for keyword in ['sell', 'price', 'profit', 'market']):
            print("🔁 Collaborating with Market Researcher...")
            market_insights = ask_agent("market_researcher", user_input)
            collaborative_note = f"\n\n📈 Market Researcher says:\n{market_insights}\n"

        elif any(keyword in user_input.lower() for keyword in ['rain', 'temperature', 'weather', 'irrigation']):
            print("🔁 Collaborating with Weather Station...")
            weather_insights = ask_agent("weather_station", user_input)
            collaborative_note = f"\n\n🌦️ Weather Station says:\n{weather_insights}\n"

        else:
            collaborative_note = ""

        prompt = f"""
You are a helpful farming advisor focused on sustainability and resource optimization.
Use the dataset below and collaborate with other experts if needed to suggest what crop the farmer should grow.

DATASET:
{top_rows}

QUESTION:
{user_input}
{collaborative_note}
"""

        response = ollama.chat(
            model='phi',
            messages=[
                {'role': 'system', 'content': 'You are a helpful and smart farmer advisor.'},
                {'role': 'user', 'content': prompt}
            ]
        )

        return response['message']['content']

    except Exception as e:
        return f"Error while processing advice: {e}"

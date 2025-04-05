# agents/multi_agent_router.py

def ask_agent(agent_name, question):
    if agent_name == "market_researcher":
        from agents.market_researcher import get_market_insights
        return get_market_insights(question)
    elif agent_name == "weather_station":
        from agents.weather_station import get_weather_info
        return get_weather_info(question)
    else:
        return "Agent not recognized for collaboration."

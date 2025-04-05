from flask import Flask, render_template, request
from agents import farmer_advisor, market_researcher, weather_station
from utils.db import init_db, log_interaction

app = Flask(__name__, template_folder="app/templates")
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        agent = request.form.get("agent")
        query = request.form.get("query")

        if agent == "farmer_advisor":
            response = farmer_advisor.get_advice(query)

        elif agent == "market_researcher":
            response = market_researcher.get_market_insights(query)

        elif agent == "weather_station":
            response = weather_station.get_weather_info(query)

        elif agent == "multi_agent":
            market_response = market_researcher.get_market_insights(query)
            weather_response = weather_station.get_weather_info(query)
            response = f"📊 Market says:\n{market_response}\n\n🌦️ Weather says:\n{weather_response}"

        log_interaction(agent, query, response)

    return render_template("index.html", response=response)

# 👇 ADD THIS TO MAKE IT RUN
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Blueprint, render_template, request
from agents import farmer_advisor, market_researcher, weather_station
from utils.db import log_interaction, init_db

main = Blueprint('main', __name__)
init_db()

@main.route('/', methods=['GET', 'POST'])
def index():
    response = None
    if request.method == 'POST':
        agent = request.form.get('agent')
        question = request.form.get('question')

        if agent == 'farmer_advisor':
            response = farmer_advisor.get_advice(question)
        elif agent == 'market_researcher':
            response = market_researcher.get_market_insights(question)
        elif agent == 'weather_station':
            response = weather_station.get_weather_info(question)

        log_interaction(agent, question, response)

    return render_template('index.html', response=response)

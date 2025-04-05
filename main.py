from agents import farmer_advisor, market_researcher, weather_station
from utils.db import init_db, log_interaction

def main():
    init_db()
    print("🌱 Welcome to AgriAdvisor - Sustainable Farming AI\n")

    while True:
        print("\nAgents Available:")
        print("1. Farmer Advisor")
        print("2. Market Researcher")
        print("3. Weather Station")
        print("4. Multi-Agent Query (Market + Weather)")
        print("0. Exit")
        choice = input("Choose an agent [1/2/3/4/0]: ").strip()

        if choice == "1":
            user_input = input("\n🧑‍🌾 Enter your question for the Farmer Advisor: ").strip()
            print("\n🤖 Generating response...")
            response = farmer_advisor.get_advice(user_input)
            print(f"\n🧠 Advisor says:\n{response}")
            log_interaction("farmer_advisor", user_input, response)

        elif choice == "2":
            user_input = input("\n📈 Enter your question for the Market Researcher: ").strip()
            print("\n🤖 Generating response...")
            response = market_researcher.get_market_insights(user_input)
            print(f"\n📊 Market Researcher says:\n{response}")
            log_interaction("market_researcher", user_input, response)

        elif choice == "3":
            user_input = input("\n🌦️ Enter your question for the Weather Station: ").strip()
            print("\n🤖 Generating response...")
            response = weather_station.get_weather_info(user_input)
            print(f"\n🌤️ Weather Station says:\n{response}")
            log_interaction("weather_station", user_input, response)

        elif choice == "4":
            user_input = input("\n🤝 Enter your multi-agent query: ").strip()
            print("\n🤖 Asking Market Researcher and Weather Station...")

            market_response = market_researcher.get_market_insights(user_input)
            weather_response = weather_station.get_weather_info(user_input)

            combined_response = f"📊 Market says:\n{market_response}\n\n🌦️ Weather says:\n{weather_response}"
            print(f"\n🧠 Combined Response:\n{combined_response}")

            log_interaction("market_researcher,weather_station", user_input, combined_response)

        elif choice == "0":
            print("👋 Exiting. Have a sustainable day!")
            break

        else:
            print("❌ Invalid option. Try again.")

if __name__ == '__main__':
    main()

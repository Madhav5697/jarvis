import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city="Hospet"):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        response = requests.get(url)
        data = response.json()

        location = data["location"]["name"]
        region = data["location"]["region"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        feels_like = data["current"]["feelslike_c"]
        humidity = data["current"]["humidity"]
        wind_kph = data["current"]["wind_kph"]

        return (
            f"In {location}, {region}, it's currently {temp_c}°C with {condition}. "
            f"It feels like {feels_like}°C, humidity is {humidity}%, and wind speed is {wind_kph} kilometers per hour."
        )

    except Exception as e:
        print(f"❌ Error fetching weather: {e}")
        return "Apologies sir, I couldn't fetch the weather right now."

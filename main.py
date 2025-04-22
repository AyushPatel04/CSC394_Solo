from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to my API"}

@app.get("/suggestion")
def get_weather_suggestion():
    # Chicago coordinates as an example
    latitude = 41.87
    longitude = -87.62

    # Call Open-Meteo's weather API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    weather_data = response.json()

    temp_c = weather_data["current_weather"]["temperature"]
    condition_code = weather_data["current_weather"]["weathercode"]

    # Smart suggestion based on weather
    if temp_c > 25:
        suggestion = "It's hot outside — stay hydrated or go swimming!"
    elif temp_c > 15:
        suggestion = "Perfect weather for a walk or jog!"
    else:
        suggestion = "It’s chilly — maybe stay in and drink something warm."

    return {
        "temperature": f"{temp_c}°C",
        "suggestion": suggestion
    }


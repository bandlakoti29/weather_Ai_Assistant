import requests
import os
from langchain.tools import tool
from functools import lru_cache

# ✅ Base URLs (CLEAN — no placeholders)
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


# ✅ Cache Function (fixed)
@lru_cache(maxsize=100)
def fetch_data(url, params_tuple):
    try:
        params = dict(params_tuple)  # convert tuple → dict
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# 🌦️ Current Weather Tool
@tool
def get_weather(city: str) -> str:
    """Get current weather details of a city"""

    params = {
        "q": city,
        "appid": os.getenv("WEATHER_API_KEY"),
        "units": "metric"
    }

    data = fetch_data(WEATHER_URL, tuple(params.items()))

    # ❌ API error
    if "error" in data:
        return f"Error: {data['error']}"

    # ❌ City not found / API issue
    if data.get("cod") != 200:
        return f"Error: {data.get('message')}"

    return f"""
City: {city}
Temperature: {data['main']['temp']}°C
Feels Like: {data['main']['feels_like']}°C
Humidity: {data['main']['humidity']}%
Weather: {data['weather'][0]['description']}
"""


# 📅 Forecast Tool
@tool
def get_forecast(city: str) -> str:
    """Get 5-day weather forecast of a city"""

    params = {
        "q": city,
        "appid": os.getenv("WEATHER_API_KEY"),
        "units": "metric"
    }

    data = fetch_data(FORECAST_URL, tuple(params.items()))

    # ❌ API error
    if "error" in data:
        return f"Error: {data['error']}"

    # ❌ City/API issue
    if data.get("cod") != "200":
        return f"Error: {data.get('message')}"

    forecast_list = data["list"][:5]

    result = "Forecast:\n"
    for item in forecast_list:
        result += f"{item['dt_txt']} → {item['main']['temp']}°C, {item['weather'][0]['description']}\n"

    return result


# 🌡️ Conversion Tool
@tool
def convert_c_to_f(temp: float) -> str:
    """Convert Celsius to Fahrenheit"""
    return f"{(temp * 9/5) + 32:.2f} °F"
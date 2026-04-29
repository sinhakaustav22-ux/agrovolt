import httpx
import os
from dotenv import load_dotenv

load_dotenv()
OWM_KEY = os.getenv("OPENWEATHER_API_KEY", "")


async def get_weather(lat: float, lon: float) -> dict:
    """Fetch current weather from OpenWeatherMap."""
    if not OWM_KEY:
        # Return mock data if no key set
        return {
            "temperature": 28.5,
            "humidity": 62,
            "rainfall": 0.0,
            "description": "Clear sky (mock data - add API key in .env)",
            "wind_speed": 3.2,
            "location": f"Lat {lat}, Lon {lon}"
        }

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={OWM_KEY}&units=metric"
    )
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()

    return {
        "temperature":  data["main"]["temp"],
        "humidity":     data["main"]["humidity"],
        "rainfall":     data.get("rain", {}).get("1h", 0.0),
        "description":  data["weather"][0]["description"].title(),
        "wind_speed":   data["wind"]["speed"],
        "location":     data.get("name", "Unknown")
    }

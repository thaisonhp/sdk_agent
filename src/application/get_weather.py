import requests
from agents import function_tool
import os 
API_KEY = os.getenv("API_KEY_OPENWEATHERMAP")

@function_tool
def get_the_weather_today(location: str) -> str:
    """Lấy thông tin thời tiết theo vị trí."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"Thời tiết tại {location} hôm nay: {weather_desc}, {temp}°C."
    else:
        return f"Không thể lấy thông tin thời tiết cho {location}."

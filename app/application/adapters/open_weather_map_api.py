import requests
from datetime import datetime
from typing import Optional, Tuple

from app.config import Settings

settings = Settings()


class OpenWeatherMapAPI:
    def __init__(self):
        self.api_key = settings.API_KEY_OPENWEATHERMAP
        self.base_url = "https://api.openweathermap.org/data/3.0"

    def _make_request(self, endpoint: str, params: dict) -> Optional[dict]:
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return None

    def get_coordinates(self, city: str) -> Optional[dict]:
        endpoint = "http://api.openweathermap.org/geo/1.0/direct"
        params = {"q": city, "limit": 1, "appid": self.api_key}
        return self._make_request(endpoint, params)

    def get_weather_data(self, lat: float, lon: float, exclude: str) -> Optional[dict]:
        endpoint = f"{self.base_url}/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "exclude": exclude,
            "appid": self.api_key,
            "units": "metric",
        }
        return self._make_request(endpoint, params)

    def get_forecast_and_data(self, city_name: str) -> Optional[Tuple[str, dict]]:
        geo_data = self.get_coordinates(city_name)
        if not geo_data:
            return None

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        weather_data = self.get_weather_data(lat, lon, exclude="minutely,hourly")
        if not weather_data:
            return None

        current_weather = weather_data["current"]
        current_temp_celsius = round(current_weather["temp"])
        current_desc = current_weather["weather"][0]["description"]

        forecast_text = f"{current_temp_celsius}°C and {current_desc} in {city_name}. Average for the next days: "

        daily_forecast = weather_data["daily"]
        for day in daily_forecast:
            temp_celsius = round(day["temp"]["day"])
            date = datetime.fromtimestamp(day["dt"]).strftime("%d/%m")
            forecast_text += f"{temp_celsius}°C on {date}, "

        forecast_text = forecast_text[:-2]

        return forecast_text, weather_data

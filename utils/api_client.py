import requests
import datetime
import streamlit as st
from typing import Dict, List

class WeatherAPI:
    def __init__(self):
        self.base_url = "http://api.openweathermap.org/data/2.5"
        try:
            self.api_key = st.secrets["openweather_api_key"]
        except FileNotFoundError:
            st.error("⚠️ OpenWeatherMap API key not found!")
            st.info("""
                Please configure your OpenWeatherMap API key in the Streamlit secrets.
                You can get a free API key from: https://openweathermap.org/
            """)
            st.stop()

    def get_current_weather(self, city: str) -> Dict:
        """Fetch current weather data for a city"""
        return self._fetch_current_weather(city, self.api_key, self.base_url)

    def get_historical_weather(self, city: str, days: int) -> List[Dict]:
        """Fetch historical weather data for a city"""
        return self._fetch_historical_weather(city, days, self.api_key, self.base_url)

    @staticmethod
    @st.cache_data(ttl=600)  # Cache for 10 minutes
    def _fetch_current_weather(city: str, api_key: str, base_url: str) -> Dict:
        """Internal method to fetch current weather data"""
        try:
            url = f"{base_url}/weather"
            params = {
                "q": city,
                "appid": api_key,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            return {
                "temp": round(data["main"]["temp"], 1),
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"]
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch current weather: {str(e)}")

    @staticmethod
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def _fetch_historical_weather(city: str, days: int, api_key: str, base_url: str) -> List[Dict]:
        """Internal method to fetch historical weather data"""
        try:
            url = f"{base_url}/forecast"
            params = {
                "q": city,
                "appid": api_key,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            processed_data = []
            for item in data["list"][:days * 8]:  # 8 data points per day
                processed_data.append({
                    "datetime": datetime.datetime.fromtimestamp(item["dt"]),
                    "temp": item["main"]["temp"],
                    "humidity": item["main"]["humidity"],
                    "pressure": item["main"]["pressure"],
                    "condition": item["weather"][0]["main"]
                })
            return processed_data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch historical weather: {str(e)}")
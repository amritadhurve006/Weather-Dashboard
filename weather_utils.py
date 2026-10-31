import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://open-meteo.com/en/docs"  # Open-Meteo API endpoint
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WMO Weather Interpretation Codes
WMO_CODE_MAP = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️",
    2: "Partly cloudy ⛅",
    3: "Overcast ☁️",
    45: "Foggy 🌫️",
    48: "Depositing rime fog 🌫️",
    51: "Light drizzle 🌧️",
    53: "Moderate drizzle 🌧️",
    55: "Dense drizzle 🌧️",
    61: "Slight rain 🌧️",
    63: "Moderate rain 🌧️",
    65: "Heavy rain 🌧️",
    71: "Slight snow 🌨️",
    73: "Moderate snow 🌨️",
    75: "Heavy snow 🌨️",
    80: "Slight rain showers 🌦️",
    81: "Moderate rain showers 🌦️",
    82: "Violent rain showers ⛈️",
    95: "Thunderstorm 🌩️",
    96: "Thunderstorm with light hail ⛈️",
    99: "Thunderstorm with heavy hail ⛈️",
}

def weather_condition(code: int) -> str:
    """Translates WMO weather code into human-readable description."""
    return WMO_CODE_MAP.get(code, "Unknown Condition 🌤️")

def search_city(city_name: str):
    """Searches latitude and longitude for a given city name using Open-Meteo Geocoding API."""
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    response = requests.get(GEOCODING_URL, params=params, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "name": result.get("name"),
                "country": result.get("country", ""),
                "latitude": result.get("latitude"),
                "longitude": result.get("longitude"),
                "timezone": result.get("timezone", "auto")
            }
    return None

def get_live_weather(lat: float, lon: float, timezone: str = "auto"):
    """Fetches live, hourly, and daily weather forecast data from Open-Meteo API."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m"
        ],
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation_probability",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
            "uv_index"
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum"
        ],
        "timezone": timezone
    }
    response = requests.get(FORECAST_URL, params=params, timeout=10)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch weather data (Status code: {response.status_code})")
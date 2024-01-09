# shared/config/external_api_config.py
import os

# Constants for configuration keys
API_URL_ENV_KEY = "API_URL_ENV"
API_KEY_ENV_KEY = "API_KEY_ENV"
ELASTICSEARCH_INDEX_ENV_KEY = "ELASTICSEARCH_INDEX_ENV"

# Constants for default values
DEFAULT_EXCHANGERATES_API_KEY = os.getenv("EXCHANGERATES_API_KEY")
DEFAULT_WEATHER_API_LOCATION = os.getenv("WEATHER_API_LOCATION")

exchangerates_config = {
    API_URL_ENV_KEY: "EXCHANGERATES_API_URL",
    API_KEY_ENV_KEY: "EXCHANGERATES_API_KEY",
    ELASTICSEARCH_INDEX_ENV_KEY: "ELASTICSEARCH_EXCHANGERATES_INDEX_NAME",
    "QUERY_PARAMS": {"access_key": DEFAULT_EXCHANGERATES_API_KEY},
    "parse_function": lambda data: {
        "success": data.get("success", False),
        "timestamp": data.get("timestamp"),
        "base_currency": data.get("base"),
        "date": data.get("date"),
        "exchange_rates": data.get("rates", {}),
    },
}

weather_config = {
    API_URL_ENV_KEY: "WEATHER_API_URL",
    API_KEY_ENV_KEY: "WEATHER_API_KEY",
    ELASTICSEARCH_INDEX_ENV_KEY: "ELASTICSEARCH_WEATHER_INDEX_NAME",
    "QUERY_PARAMS": {"q": DEFAULT_WEATHER_API_LOCATION},
    "parse_function": lambda data: {
        "location_name": data["location"]["name"],
        "temperature_c": data["current"]["temp_c"],
        "weather_condition": data["current"]["condition"]["text"],
    },
}

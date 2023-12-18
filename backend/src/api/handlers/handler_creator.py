# backend/src/api/handlers/handler_creator.py
from .api_handler import create_api_handler, create_get_data_handler
from .config.api_configs import exchangerates_config, weather_config

# Create handlers for each API
for api_name, api_config in [
    ("exchangeratesapi", exchangerates_config),
    ("weatherapi", weather_config),
]:
    create_api_handler(api_name, api_config)
    create_get_data_handler(api_name, api_config)

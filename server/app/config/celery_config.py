# server/app/config/celery_config.py
from datetime import timedelta


class CeleryConfig:
    beat_schedule = {
        "fetch-weather-data-every-15-minutes": {
            "task": "server.app.tasks.scheduled_tasks.fetch_weather_data",
            "schedule": timedelta(minutes=15),
        },
        "fetch-exchange-rates-data-daily": {
            "task": "server.app.tasks.scheduled_tasks.fetch_exchange_rates_data",
            "schedule": timedelta(hours=24),
        },
    }

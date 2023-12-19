# backend/src/api/main.py
from fastapi_utils.tasks import repeat_every
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from src.api.config.app_config import configure_app
from src.api.config.elasticsearch_config import check_elasticsearch
from src.api.config.log_config import configure_logging
from src.api.handlers.api_handler import (
    create_api_handler,
    create_get_data_handler,
    exchangerates_config,
    weather_config,
)

# Call the configure_logging function
configure_logging()

app = configure_app()

# Metrics
Instrumentator().instrument(app).expose(app)


# Routers list
routers = [
    create_api_handler("exchangeratesapi", exchangerates_config),
    create_get_data_handler("exchangeratesapi", exchangerates_config),
    create_api_handler("weatherapi", weather_config),
    create_get_data_handler("weatherapi", weather_config),
]

# Loop through the routes
for router in routers:
    app.include_router(router)

# Define a list of scheduled tasks
scheduled_tasks = [
    {
        "handler": "create_api_handler",
        "function": "create_api_handler.fetch_translate_store_data",
        "api_name": "exchangeratesapi",
        "interval_seconds": 60 * 60 * 24,
    },
    {
        "handler": "create_api_handler",
        "function": "create_api_handler.fetch_translate_store_data",
        "api_name": "weatherapi",
        "interval_seconds": 60 * 30,  # Run every 30 minutes
    },
]


def scheduled_task(api_name, scheduled_function):
    try:
        scheduled_function(api_name)
    except Exception as e:
        logger.error(f"Error in scheduled task: {str(e)}")


# Event handler for application startup
# Event handler for application startup
def startup_event():
    logger.info("Application is starting")
    check_elasticsearch()

    logger.info("Application has started")


# Event handler for application shutdown
def shutdown_event():
    logger.info("Application is shutting down")


# Register startup and shutdown event handlers
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

# If the script is run directly (not imported)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

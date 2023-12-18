# backend/main.py
from config.app_config import configure_app
from config.elasticsearch_config import check_elasticsearch
from config.log_config import configure_logging
from fastapi_utils.tasks import repeat_every
from handlers.api_handler import fetch_translate_store_exchangerate_data
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator, metrics

# Call the configure_logging function
configure_logging()

app = configure_app()

# Metrics
Instrumentator().instrument(app).expose(app)


# Define a list of scheduled tasks
scheduled_tasks = [
    {
        "handler": "handlers.api_handler",
        "function": "fetch_translate_store_exchangerate_data",
        "api_name": "exchangeratesapi",
        "interval_seconds": 60 * 60 * 24,
    },
    {
        "handler": "handlers.api_handler",
        "function": "fetch_translate_store_weather_data",
        "interval_seconds": 60 * 30,  # Run every 30 minutes
    },
]


def scheduled_task(api_name, scheduled_function):
    try:
        scheduled_function(api_name)
    except Exception as e:
        logger.error(f"Error in scheduled task: {str(e)}")


# Event handler for application startup
def startup_event():
    logger.info("Application is starting")
    check_elasticsearch()

    # Schedule tasks
    for task in scheduled_tasks:
        handler_module = __import__(task["handler"], fromlist=[task["function"]])
        scheduled_function = getattr(handler_module.router, task["function"])

        @repeat_every(seconds=task["interval_seconds"], logger=None)
        def scheduled_task():
            try:
                scheduled_function(task["api_name"])
            except Exception as e:
                logger.error(f"Error in scheduled task: {str(e)}")

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

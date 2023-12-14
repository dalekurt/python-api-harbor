# backend/main.py
import time

from config.app_config import configure_app
from config.elasticsearch_config import check_elasticsearch
from fastapi_utils.tasks import repeat_every
from loguru import logger

app = configure_app()

logger.add("logs/app.log", rotation="500 MB", level="INFO")


# Event handler for application startup
def startup_event():
    logger.info("Application is starting")
    check_elasticsearch()

    # Schedule the task to run every day at a specific time
    @repeat_every(seconds=60 * 60 * 24, logger=None)  # Run every 24 hours
    def scheduled_task():
        try:
            from handlers.exchangerates_handler import fetch_translate_store_data

            fetch_translate_store_data()
        except Exception as e:
            logger.error(f"Error in scheduled task: {str(e)}")

    # Run the scheduled task when the application starts
    scheduled_task()
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

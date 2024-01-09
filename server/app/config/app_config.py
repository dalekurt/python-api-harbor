# server/app/config/app_config.py
import asyncio
import os

from app.crons.schedule_exchangerates_workflow import schedule_exchangerates_workflow
from app.crons.schedule_weather_workflow import schedule_weather_workflow
from app.routes import exchangerates_routes, weather_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.config.logger_config import logger


async def start_scheduled_workflows():
    """Start scheduled workflows with error handling and enhanced logging."""
    # Schedule Exchange Rates Workflow
    try:
        await schedule_exchangerates_workflow()
        logger.info("Exchange Rates workflow scheduled successfully.")
    except Exception as e:
        logger.error(f"Failed to schedule Exchange Rates workflow: {e}")

    # Schedule Weather Workflow
    try:
        await schedule_weather_workflow()
        logger.info("Weather workflow scheduled successfully.")
    except Exception as e:
        logger.error(f"Failed to schedule Weather workflow: {e}")


def configure_app() -> FastAPI:
    app = FastAPI()

    essential_variables = [
        "EXCHANGERATES_API_URL",
        "EXCHANGERATES_API_KEY",
        "WEATHER_API_URL",
        "WEATHER_API_LOCATION",
    ]

    # Check for the the essential environment variables
    missing_variables = [var for var in essential_variables if os.getenv(var) is None]
    if missing_variables:
        raise EnvironmentError(
            f"Missing environment variables: {', '.join(missing_variables)}"
        )

    # Configure CORS
    origins = ["http://localhost:8001"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Lifecycle event handlers
    app.add_event_handler("startup", startup_event_handler)
    app.add_event_handler("shutdown", shutdown_event_handler)

    # Routers
    app.include_router(exchangerates_routes.router, prefix="")
    app.include_router(weather_routes.router, prefix="")

    return app


async def startup_event_handler():
    logger.info("Starting server")
    asyncio.create_task(schedule_exchangerates_workflow())
    asyncio.create_task(schedule_weather_workflow())
    logger.info("Scheduled workflows initiated")


async def shutdown_event_handler():
    logger.info("Shutting down server")
    logger.info("Shutdown complete")

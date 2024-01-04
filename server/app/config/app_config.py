# server/app/config/app_config.py
import os

from app.config.lifespan_config import shutdown_event_handler, startup_event_handler
from app.routes.api_routes import router as api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def configure_app() -> FastAPI:
    app = FastAPI()

    essential_variables = [
        "EXCHANGERATES_API_URL",
        "EXCHANGERATES_API_KEY",
        "WEATHER_API_URL",
        "WEATHER_API_LOCATION",
    ]

    # Check for the presence of essential environment variables
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

    app.add_event_handler("startup", startup_event_handler)
    app.add_event_handler("shutdown", shutdown_event_handler)

    app.include_router(api_router, prefix="")

    return app

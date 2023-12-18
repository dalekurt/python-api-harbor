# backend/src/api/config/app_config.py
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handlers.api_handler import router as api_router  # Change the import here


def configure_app() -> FastAPI:
    app = FastAPI()

    essential_variables = [
        "EXCHANGERATES_API_URL",
        "EXCHANGERATES_API_KEY",
        "WEATHER_API_URL",
        "WEATHER_API_LOCATION",
    ]
    # Check for the presence of essential environment variables
    for var in essential_variables:
        value = os.getenv(var)
        if value is None:
            raise EnvironmentError(
                f"Environment variable '{var}' is missing. Please set it."
            )

    # Include routers
    app.include_router(api_router, prefix="/api")

    # Configure CORS
    origins = ["http://localhost:8001"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

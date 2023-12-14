# backend/config/app_config.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handlers.api_handler import router as exchangerates_router


def configure_app() -> FastAPI:
    app = FastAPI()

    # Include routers
    app.include_router(exchangerates_router)

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

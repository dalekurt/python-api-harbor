# server/app/handlers/handler_creator.py

from app.handlers.exchangerates_handler import router as exchangerates_handler
from app.handlers.weather_handler import router as weather_handler

# Routers list
routers = [
    exchangerates_handler,
    weather_handler,
]


def create_handlers(app):
    """
    Create and attach handlers to the FastAPI app.
    """
    for router in routers:
        app.include_router(router, prefix="/v1")

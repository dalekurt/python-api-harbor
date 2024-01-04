# server/main.py
from app.config.app_config import configure_app
from app.handlers import exchangerates_handler, weather_handler
from dotenv import load_dotenv

# NOTE: Moved all the app configuration to app/config/app_config.py

# Load the .env file
load_dotenv()

app = configure_app()

# Include the new handler routers
app.include_router(exchangerates_handler.router)
app.include_router(weather_handler.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

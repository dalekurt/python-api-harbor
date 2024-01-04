# server/main.py
from app.config.app_config import configure_app
from app.routes import exchangerates_routes, weather_routes
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

app = configure_app()

# Routers
app.include_router(exchangerates_routes.router, prefix="")
app.include_router(weather_routes.router, prefix="")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

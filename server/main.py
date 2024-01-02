# server/main.py
from app.config.lifespan_config import shutdown_event_handler, startup_event_handler
from app.databases.dragonflydb import get_redis
from app.databases.temporal_client import create_temporal_client
from app.routes import api_routes
from app.routes.api_routes import router as api_router
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from loguru import logger

# Load my .env file
load_dotenv()

app = FastAPI()

app.add_event_handler("startup", startup_event_handler)
app.add_event_handler("shutdown", shutdown_event_handler)

app.include_router(api_routes.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

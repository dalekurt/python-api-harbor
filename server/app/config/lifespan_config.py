# server/app/config/lifespan_config.py
from app.config import logger_config
from fastapi import FastAPI
from loguru import logger


async def startup_event_handler():
    app = FastAPI()
    logger.info("Starting server")
    logger_config.logger.configure()


async def shutdown_event_handler():
    app = FastAPI()
    logger.info("Shutting down server")
    logger.info("Shutdown complete")

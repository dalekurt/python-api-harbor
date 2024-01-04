# server/app/config/lifespan_config.py
from fastapi import FastAPI
from loguru import logger


async def startup_event_handler():
    logger.info("Starting server")


async def shutdown_event_handler():
    logger.info("Shutting down server")
    logger.info("Shutdown complete")

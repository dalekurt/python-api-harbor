# backend/src/api/config/log_config.py

import sys

from loguru import logger


def configure_logging():
    # Configure logging to write to both console and a log file
    logger.add(sys.stdout, level="INFO")
    logger.add("logs/app.log", rotation="5 MB", level="INFO")

    logger.info("Logging configured successfully")

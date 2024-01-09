# shared/config/logger_config.py

from loguru import logger

logger.add("logs/app.log", rotation="5 MB", level="INFO", backtrace=True, diagnose=True)

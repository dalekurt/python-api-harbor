# server/app/databases/dragonflydb.py
import redis
from app.config import logger_config
from app.config.dragonflydb_config import DRAGONFLYDB_CONFIG
from fastapi import Depends
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed


async def get_redis():
    retry_config = DRAGONFLYDB_CONFIG.get("retry", {})

    @retry(**retry_config)
    def create_redis_connection():
        redis_host = DRAGONFLYDB_CONFIG["host"]
        redis_port = DRAGONFLYDB_CONFIG["port"]
        logger.info(
            f"Attempting to connect to DragonflyDB at {redis_host}:{redis_port}"
        )

        redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True,
        )
        logger.info("Successfully connected to DragonflyDB")
        return redis_client

    try:
        redis_client = create_redis_connection()
        yield redis_client
    except Exception as e:
        logger.error(f"Failed to connect to DragonflyDB: {e}")
        raise
    finally:
        logger.info("Closing DragonflyDB connection")
        if "redis_client" in locals():
            redis_client.close()

# server/app/databases/mongodb.py
import logging

from app.config.mongodb_config import MONGODB_CONFIG
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from tenacity import retry, stop_after_attempt, wait_fixed

logger = logging.getLogger(__name__)


@retry(
    wait=wait_fixed(1),
    stop=stop_after_attempt(10),
    retry=ConnectionFailure,
)
def get_mongo_client():
    try:
        client = MongoClient(
            host=MONGODB_CONFIG["host"],
            port=MONGODB_CONFIG["port"],
            username=MONGODB_CONFIG["username"],
            password=MONGODB_CONFIG["password"],
            authSource=MONGODB_CONFIG["auth_source"],
        )
        logger.info("Successfully connected to MongoDB")
        return client
    except ConnectionFailure as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise

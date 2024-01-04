# server/app/databases/celery.py
import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

dragonflydb_host = os.getenv("DRAGONFLYDB_HOST", "localhost")
dragonflydb_port = os.getenv("DRAGONFLYDB_PORT", "6379")
broker_url = f"redis://{dragonflydb_host}:{dragonflydb_port}/0"

celery_app = Celery("api_harbor_worker", broker=broker_url)

# Import and set the Celery configuration
from server.app.config.celery_config import CeleryConfig

celery_app.config_from_object(CeleryConfig)

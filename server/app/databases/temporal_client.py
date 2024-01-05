# server/app/databases/temporal_client.py
import asyncio
import os
import random
import string

from app.config.logger_config import logger
from app.config.temporal_config import TEMPORAL_CONFIG
from temporalio.client import Client
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(wait=wait_fixed(1), stop=stop_after_attempt(10))
async def create_temporal_client():
    try:
        temporal_host = TEMPORAL_CONFIG["host"]
        temporal_port = TEMPORAL_CONFIG["port"]
        workflow_client = await Client.connect(f"{temporal_host}:{temporal_port}")
        return workflow_client
    except Exception as e:
        logger.error(f"Error connecting to Temporal server: {e}")
        raise

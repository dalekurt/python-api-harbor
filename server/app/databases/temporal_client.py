# server/app/databases/temporal_client.py
from app.config.temporal_config import TEMPORAL_CONFIG
from temporalio.client import Client
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(
    wait=wait_fixed(1),
    stop=stop_after_attempt(10),
)
def create_temporal_client():
    temporal_host = TEMPORAL_CONFIG["host"]
    temporal_port = TEMPORAL_CONFIG["port"]

    workflow_client = Client.connect(f"{temporal_host}:{temporal_port}")

    return workflow_client

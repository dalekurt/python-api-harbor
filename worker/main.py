# worker/main.py
import asyncio
import os

from temporalio.client import Client
from temporalio.worker import Worker
from tenacity import before_log, retry, stop_after_attempt, wait_fixed

from shared.activities.data_activities import (
    fetch_data_activity,
    store_data_activity,
    translate_data_activity,
)
from shared.activities.simple_activity import simple_activity
from shared.clients.elasticsearch import get_elasticsearch_client
from shared.config.logger_config import logger

# from shared.workflows.exchangerates_workflow import ExchangeRatesWorkflow
# from shared.workflows.weather_workflow import WeatherWorkflow
from shared.workflows.simple_workflow import SimpleWorkflow


@retry(
    wait=wait_fixed(10), stop=stop_after_attempt(5), before=before_log(logger, "INFO")
)
async def connect_to_elasticsearch():
    logger.info("Attempting to connect to Elasticsearch...")
    await get_elasticsearch_client()
    logger.info("Successfully connected to Elasticsearch.")


@retry(
    wait=wait_fixed(10), stop=stop_after_attempt(5), before=before_log(logger, "INFO")
)
async def connect_to_temporal(temporal_host, temporal_port):
    logger.info("Attempting to connect to Temporal...")
    client = await Client.connect(f"{temporal_host}:{temporal_port}")
    logger.info("Successfully connected to Temporal.")
    return client


async def main():
    # Retrieve Temporal service address and Task Queue from environment variables
    temporal_host = os.getenv("TEMPORAL_HOST", "localhost")
    temporal_port = os.getenv("TEMPORAL_PORT", "7233")
    task_queue = os.getenv("TEMPORAL_WORKER_TASK_QUEUE", "api-queue")

    # TODO: Connect to Elasticsearch and Temporal services
    await connect_to_elasticsearch()
    client = await connect_to_temporal(temporal_host, temporal_port)

    # TODO: Create and configure the Worker
    # worker = Worker(
    #     client,
    #     task_queue=task_queue,
    #     workflows=[ExchangeRatesWorkflow, WeatherWorkflow],
    #     activities=[fetch_data_activity, translate_data_activity, store_data_activity],
    # )
    worker = Worker(
        client,
        task_queue=task_queue,
        workflows=[SimpleWorkflow],
        activities=[simple_activity],
    )

    # Log that the Worker is starting
    logger.info(f"Worker started for task queue '{task_queue}'. Listening for tasks...")

    # Run the Worker
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

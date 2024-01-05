# server/app/crons/schedule_exchangerates_workflow.py
import asyncio
import os
import random
import string

from app.databases.temporal_client import create_temporal_client
from app.workflows.exchangerates_workflow import ExchangeRatesWorkflow


async def schedule_exchangerates_workflow():
    client = await create_temporal_client()

    # Generate unique workflow ID
    id_prefix = os.getenv("EXCHANGERATES_TEMPORAL_ID", "EXCHANGERATES")
    unique_id = "".join(random.choices(string.ascii_letters + string.digits, k=9))
    workflow_id = f"{id_prefix}_{unique_id}"

    await client.execute_workflow(
        ExchangeRatesWorkflow.run,
        id=workflow_id,
        task_queue="exchangerates-task-queue",
        cron_schedule="0 */2 * * *",  # Every 2 hours
    )


# For running the scheduling directly
if __name__ == "__main__":
    asyncio.run(schedule_exchangerates_workflow())

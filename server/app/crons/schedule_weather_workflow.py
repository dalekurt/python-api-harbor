# server/app/crons/schedule_weather_workflow.py
import asyncio
import os
import random
import string

from app.databases.temporal_client import create_temporal_client
from app.workflows.weather_workflow import WeatherWorkflow


async def schedule_weather_workflow():
    client = await create_temporal_client()

    # Generate unique workflow ID
    id_prefix = os.getenv("WEATHER_API_TEMPORAL_ID", "WEATHER")
    unique_id = "".join(random.choices(string.ascii_letters + string.digits, k=9))
    workflow_id = f"{id_prefix}_{unique_id}"

    await client.execute_workflow(
        WeatherWorkflow.run,
        id=workflow_id,
        task_queue="weather-task-queue",
        cron_schedule="0 */2 * * *",  # Testing
        # cron_schedule="15 9 * * *",  # Every day at 09:15
    )


# For running the scheduling directly
if __name__ == "__main__":
    asyncio.run(schedule_weather_workflow())

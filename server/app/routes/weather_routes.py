# server/app/routes/weather_routes.py
import os

from app.databases.temporal_client import create_temporal_client
from app.handlers.weather_handler import fetch_translate_store_data, get_weather_data
from app.workflows.weather_workflow import WeatherWorkflow
from fastapi import APIRouter

router = APIRouter()

router.add_api_route("/api/weather", fetch_translate_store_data, methods=["GET"])
router.add_api_route("/data/weather", get_weather_data, methods=["GET"])


@router.get("/workflow/weather")
async def trigger_weather_workflow():
    temporal_client = await create_temporal_client()

    # Retrieve environment variables
    api_url = os.getenv("WEATHER_API_URL")
    api_key = os.getenv("WEATHER_API_KEY")
    index_name = os.getenv("ELASTICSEARCH_WEATHER_INDEX_NAME")
    workflow_id = os.getenv("WEATHER_API_TEMPORAL_ID", "default_id")
    task_queue = os.getenv("WEATHER_API_TEMPORAL_TASK_QUEUE", "default_queue")

    # Start the workflow
    workflow_handle = await temporal_client.start_workflow(
        WeatherWorkflow.run,
        [api_url, api_key, index_name],
        id=workflow_id,
        task_queue=task_queue,
    )

    return {"message": "Weather workflow triggered"}

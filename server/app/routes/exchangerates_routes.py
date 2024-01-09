# server/app/routes/exchangerates_routes.py
import os
import random
import string

from app.handlers.exchangerates_handler import (
    fetch_translate_store_data,
    get_exchangerates_data,
)
from app.workflows.exchangerates_workflow import ExchangeRatesWorkflow
from fastapi import APIRouter

from shared.clients.temporal_client import create_temporal_client

router = APIRouter()

router.add_api_route("/api/exchangerates", fetch_translate_store_data, methods=["GET"])
router.add_api_route("/data/exchangerates", get_exchangerates_data, methods=["GET"])


@router.get("/workflow/exchangerates")
async def trigger_exchange_rates_workflow():
    temporal_client = await create_temporal_client()

    # Retrieve environment variables and generate unique workflow ID
    api_url = os.getenv("EXCHANGERATES_API_URL")
    api_key = os.getenv("EXCHANGERATES_API_KEY")
    index_name = os.getenv("ELASTICSEARCH_EXCHANGERATES_INDEX_NAME")
    id_prefix = os.getenv("EXCHANGERATES_TEMPORAL_ID", "EXCHANGERATES")
    unique_id = "".join(random.choices(string.ascii_letters + string.digits, k=9))
    workflow_id = f"{id_prefix}_{unique_id}"
    task_queue = os.getenv("EXCHANGERATES_TEMPORAL_TASK_QUEUE", "default_queue")

    # Start the workflow
    workflow_handle = await temporal_client.start_workflow(
        ExchangeRatesWorkflow.run,
        [api_url, api_key, index_name],
        id=workflow_id,
        task_queue=task_queue,
    )

    return {"message": "Exchangerates workflow triggered"}

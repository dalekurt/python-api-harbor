# server/app/routes/simple_routes.py
from fastapi import APIRouter

from shared.clients.temporal_client import (
    create_temporal_client,  # Ensure this is correctly implemented to interact with Temporal
)
from shared.workflows.simple_workflow import SimpleWorkflow

router = APIRouter()


@router.post("/workflow/simple")
async def trigger_simple_workflow():
    temporal_client = await create_temporal_client()
    workflow_handle = await temporal_client.start_workflow(
        SimpleWorkflow.run, id="simple-workflow-example", task_queue="simple-task-queue"
    )
    return {"message": "Simple workflow triggered"}

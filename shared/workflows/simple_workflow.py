# shared/workflows/simple_workflow.py
from temporalio import workflow

from shared.activities.simple_activity import simple_activity


@workflow.defn
class SimpleWorkflow:
    @workflow.run
    async def run(self) -> str:
        result = await workflow.execute_activity(
            simple_activity, start_to_close_timeout=workflow.timedelta(seconds=10)
        )
        return result

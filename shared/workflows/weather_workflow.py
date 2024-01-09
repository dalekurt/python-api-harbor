# shared/app/workflows/weather_workflow.py
from datetime import timedelta

from temporalio import workflow

from shared.activities.data_activities import (
    fetch_data_activity,
    store_data_activity,
    translate_data_activity,
)


@workflow.defn
class WeatherWorkflow:
    @workflow.run
    async def run(
        self, api_url: str, api_key: str, location: str, index_name: str
    ) -> str:
        params = {"key": api_key, "q": location}

        fetched_data = await workflow.execute_activity(
            fetch_data_activity,
            api_url,
            params,
            start_to_close_timeout=timedelta(minutes=5),
        )

        translated_data = await workflow.execute_activity(
            translate_data_activity,
            fetched_data,
            start_to_close_timeout=timedelta(minutes=5),
        )

        await workflow.execute_activity(
            store_data_activity,
            translated_data,
            index_name,
            start_to_close_timeout=timedelta(minutes=5),
        )

        return "Weather data processed successfully"

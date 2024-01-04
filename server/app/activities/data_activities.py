# server/app/activities/data_activities.py
import httpx
from app.config.logger_config import logger
from app.databases.elasticsearch import get_elasticsearch_client
from temporalio import activity


# Define an activity for fetching data from an API
@activity.defn
async def fetch_data_activity(api_url: str, params: dict) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params=params)
            response.raise_for_status()
            logger.info(f"Data successfully fetched from {api_url}")
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred while fetching data: {e}")
        return {}


# Define an activity for translating or processing the fetched data
@activity.defn
async def translate_data_activity(data: dict) -> dict:
    # Implement any data translation or processing logic here
    # For this example, returning data as is
    logger.info("Data translation or processing completed")
    return data


# Define an activity for storing data in Elasticsearch
@activity.defn
async def store_data_activity(data: dict, index_name: str):
    try:
        es_client = await get_elasticsearch_client()
        response = await es_client.index(index=index_name, document=data)
        logger.info(
            f"Data successfully stored in Elasticsearch index '{index_name}': {response}"
        )
    except Exception as e:
        logger.error(f"Error occurred while storing data: {e}")

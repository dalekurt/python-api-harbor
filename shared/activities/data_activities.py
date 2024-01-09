# shared/activities/data_activities.py
import httpx
from temporalio import activity

from shared.config.logger_config import logger


@activity.defn
async def fetch_data_activity(api_url: str, params: dict) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params=params)
            response.raise_for_status()
            logger.info(f"Data successfully fetched from {api_url}")
            return response.json()
    # except httpx.HTTPError as e:
    except Exception as e:
        logger.error(f"HTTP error occurred while fetching data: {e}")
        return {}


@activity.defn
async def translate_data_activity(data: dict) -> dict:
    logger.info("Data translation or processing completed")
    return data


@activity.defn
async def store_data_activity(data: dict, index_name: str):
    from shared.clients.elasticsearch import get_elasticsearch_client

    try:
        es_client = await get_elasticsearch_client()
        response = await es_client.index(index=index_name, document=data)
        logger.info(
            f"Data successfully stored in Elasticsearch index '{index_name}': {response}"
        )
    except Exception as e:
        logger.error(f"Error occurred while storing data: {e}")

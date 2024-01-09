# server/app/handlers/weather_handler.py
import os

import aiohttp
from fastapi import HTTPException

from shared.clients.elasticsearch import (
    create_index_if_not_exists,
    get_elasticsearch_client,
)
from shared.config.external_api_config import weather_config
from shared.config.logger_config import logger


async def fetch_translate_store_data():
    async with aiohttp.ClientSession() as session:
        try:
            api_url = os.getenv(weather_config["API_URL_ENV"])
            api_key = os.getenv(weather_config["API_KEY_ENV"])
            if not api_url or not api_key:
                raise HTTPException(
                    status_code=500, detail="Weather API configuration not provided"
                )

            location = os.getenv("WEATHER_API_LOCATION")
            if not location:
                raise HTTPException(
                    status_code=500, detail="Weather API location not provided"
                )

            api_params = {"key": api_key, "q": location}
            response = await session.get(api_url, params=api_params)
            response.raise_for_status()
            data = await response.json()

            data_to_store = weather_config["parse_function"](data)

            index_name = os.getenv(
                weather_config["ELASTICSEARCH_INDEX_ENV"], "weatherapi"
            )
            await create_index_if_not_exists(index_name)

            es = await get_elasticsearch_client()
            await es.index(index=index_name, body=data_to_store)

            logger.info("Data stored in Elasticsearch successfully for weatherapi")
            return {
                "message": "Data fetched, translated, and stored successfully for weatherapi",
                "data": data_to_store,
            }
        except HTTPException as e:
            logger.error(f"HTTPException: {e.status_code} - {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_weather_data():
    try:
        index_name = os.getenv("ELASTICSEARCH_WEATHER_INDEX_NAME", "weatherapi")
        es = await get_elasticsearch_client()
        response = await es.search(index=index_name, body={"query": {"match_all": {}}})
        data = [hit["_source"] for hit in response["hits"]["hits"]]
        return {"data": data}
    except Exception as e:
        logger.error(f"Error retrieving weather data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

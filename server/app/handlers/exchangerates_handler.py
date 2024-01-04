# server/app/handlers/exchangerates_handler.py
import os

import aiohttp
from app.config.external_api_config import exchangerates_config
from app.config.logger_config import logger
from app.databases.elasticsearch import (
    create_index_if_not_exists,
    fetch_data_from_elasticsearch,
    get_elasticsearch_client,
)
from app.handlers.api_utils import fetch_data_from_api
from elasticsearch import ApiError
from fastapi import APIRouter, HTTPException

router = APIRouter()


async def fetch_data_from_api(api_url, params, session=None):
    try:
        async with session.get(api_url, params=params) if session else aiohttp.get(
            api_url, params=params
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise aiohttp.ClientResponseError(
                    status=response.status,
                    message=response.reason,
                    headers=response.headers,
                )
    finally:
        pass


@router.get("/api/exchangerates")
async def fetch_translate_store_data():
    try:
        # Use a context manager to create the aiohttp.ClientSession
        async with aiohttp.ClientSession() as session:
            # Load the Exchange Rates API configuration from environment variables
            api_url = os.getenv(exchangerates_config["API_URL_ENV"])
            api_key = os.getenv(exchangerates_config["API_KEY_ENV"])

            if not api_url or not api_key:
                raise HTTPException(
                    status_code=500,
                    detail=f"Exchange Rates API configuration not provided",
                )

            # Fetch data from the Exchange Rates API using the session
            api_params = {"access_key": api_key}
            data = await fetch_data_from_api(api_url, api_params, session=session)

            # Parsing the received JSON data
            # You can customize this part based on the actual response structure
            data_to_store = exchangerates_config["parse_function"](data)

            # Create the index if it does not exist
            index_name = os.getenv(
                exchangerates_config["ELASTICSEARCH_INDEX_ENV"], "exchangerates"
            )
            try:
                await create_index_if_not_exists(index_name)
            except ApiError as e:  # Use the updated exception class
                logger.error(f"Error creating Elasticsearch index: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")

            # Storing the data in Elasticsearch
            # Log the data to be stored
            logger.info(f"Storing data in Elasticsearch: {data_to_store}")

            # Use the Elasticsearch client to index the data
            es = get_elasticsearch_client()
            await es.index(index=index_name, body=data_to_store)

            logger.info(f"Data stored in Elasticsearch successfully for exchangerates")
            logger.info(
                f"Data fetched, translated, and stored successfully for exchangerates"
            )
            return {
                "message": "Data fetched, translated, and stored successfully for exchangerates",
                "data": data_to_store,
            }
    except HTTPException as e:
        logger.error(f"HTTPException: {e.status_code} - {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/data/exchangerates")
async def get_exchangerates_data():
    try:
        index_name = os.getenv(
            "ELASTICSEARCH_EXCHANGERATES_INDEX_NAME", "exchangeratesapi"
        )
        data = await fetch_data_from_elasticsearch(index_name)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

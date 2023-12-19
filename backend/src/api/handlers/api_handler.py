# backend/src/api/handlers/api_handler.py
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from loguru import logger
from src.api.config.elasticsearch_config import (
    create_index_if_not_exists,
    es,
    fetch_data_from_elasticsearch,
)

from .data_handler import fetch_data_from_api

load_dotenv()

router = APIRouter()


def create_api_handler(api_name, api_config):
    """
    Create an API handler for the given API.
    """

    @router.get(f"/api/{api_name}")
    async def fetch_translate_store_data():
        try:
            # Load the API configuration from environment variables
            api_url = os.getenv(api_config["API_URL_ENV"])
            api_key = os.getenv(api_config["API_KEY_ENV"])
            api_params = api_config.get("QUERY_PARAMS", {})

            if not api_url or not api_key:
                raise HTTPException(
                    status_code=500, detail=f"{api_name} API configuration not provided"
                )

            # Add API key to parameters
            api_params["key"] = api_key

            # Fetch data from the API
            data = await fetch_data_from_api(api_url, api_params)

            # Parsing the received JSON data
            # You can customize this part based on the actual response structure
            data_to_store = api_config["parse_function"](data)

            # Create the index if it does not exist
            index_name = os.getenv(api_config["ELASTICSEARCH_INDEX_ENV"], api_name)
            try:
                create_index_if_not_exists(index_name)
            except Exception as e:
                logger.error(f"Error creating Elasticsearch index: {str(e)}")

            # Storing the data in Elasticsearch
            # Log the data to be stored
            logger.info(f"Storing data in Elasticsearch: {data_to_store}")

            # Use the Elasticsearch client to index the data
            es.index(index=index_name, body=data_to_store)

            logger.info(f"Data stored in Elasticsearch successfully for {api_name}")
            logger.info(
                f"Data fetched, translated, and stored successfully for {api_name}"
            )
            return {
                "message": f"Data fetched, translated, and stored successfully for {api_name}",
                "data": data_to_store,
            }
        except HTTPException as e:
            logger.error(f"HTTPException: {e.status_code} - {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return router


def create_get_data_handler(api_name, api_config):
    """
    Create a handler to get data from Elasticsearch for the given API.
    """

    @router.get(f"/data/{api_name}")
    async def get_api_data(api_name: str):
        try:
            # Fetch data from Elasticsearch with a dynamic index name
            data = fetch_data_from_elasticsearch(
                index_name=os.getenv(api_config["ELASTICSEARCH_INDEX_ENV"], api_name)
            )
            return {"message": f"{api_name} data fetched successfully", "data": data}
        except Exception as e:
            return {"message": f"Error: {str(e)}"}

    return router


# Configuration for Exchangerates API
exchangerates_config = {
    "API_URL_ENV": "EXCHANGERATES_API_URL",
    "API_KEY_ENV": "EXCHANGERATES_API_KEY",
    "ELASTICSEARCH_INDEX_ENV": "ELASTICSEARCH_EXCHANGERATES_INDEX_NAME",
    "QUERY_PARAMS": {"access_key": os.getenv("EXCHANGERATES_API_KEY")},
    "parse_function": lambda data: {
        "success": data.get("success", False),
        "timestamp": data.get("timestamp"),
        "base_currency": data.get("base"),
        "date": data.get("date"),
        "exchange_rates": data.get("rates", {}),
    },
}

# Configuration for Weather API
weather_config = {
    "API_URL_ENV": "WEATHER_API_URL",
    "API_KEY_ENV": "WEATHER_API_KEY",
    "ELASTICSEARCH_INDEX_ENV": "ELASTICSEARCH_WEATHER_INDEX_NAME",
    "QUERY_PARAMS": {"q": os.getenv("WEATHER_API_LOCATION")},
    "parse_function": lambda data: {
        "location_name": data["location"]["name"],
        "temperature_c": data["current"]["temp_c"],
        "weather_condition": data["current"]["condition"]["text"],
    },
}

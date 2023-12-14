# backend/src/api/handlers/api_handler.py
import os

from config.elasticsearch_config import (
    create_index_if_not_exists,
    es,
    fetch_data_from_elasticsearch,
)
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from loguru import logger

from .data_handler import fetch_data_from_api

load_dotenv()

router = APIRouter()


@router.get("/exchangeratesapi")
async def fetch_translate_store_exchangerates_data():
    try:
        # Load the API configuration from environment variables
        api_url = os.getenv("EXCHANGERATES_API_URL")
        api_key = os.getenv("EXCHANGERATES_API_KEY")

        if not api_url or not api_key:
            raise HTTPException(
                status_code=500, detail="API configuration not provided"
            )

        # Fetch data from the Exchange Rates API
        params = {"access_key": api_key}
        data = await fetch_data_from_api(api_url, params)

        # Parsing the received JSON data
        success = data.get("success", False)
        timestamp = data.get("timestamp")
        base_currency = data.get("base")
        date = data.get("date")
        exchange_rates = data.get("rates", {})

        data_to_store = {
            "success": success,
            "timestamp": timestamp,
            "base_currency": base_currency,
            "date": date,
            "exchange_rates": exchange_rates,
        }

        # Create the index if it does not exist
        try:
            create_index_if_not_exists()
        except Exception as e:
            logger.error(f"Error creating Elasticsearch index: {str(e)}")

        # Storing the data in Elasticsearch
        index_name = os.getenv("ELASTICSEARCH_INDEX_NAME", "exchangeratesapi")

        # Log the data to be stored
        logger.info(f"Storing data in Elasticsearch: {data_to_store}")

        # Use the Elasticsearch client to index the data
        es.index(index=index_name, body=data_to_store)

        logger.info("Data stored in Elasticsearch successfully")
        logger.info("Data fetched, translated, and stored successfully")
        return {
            "message": "Data fetched, translated, and stored successfully",
            "data": data_to_store,
        }
    except HTTPException as e:
        logger.error(f"HTTPException: {e.status_code} - {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/exchangeratesdata")
async def get_exchange_rates_data():
    try:
        # Fetch data from Elasticsearch with a dynamic index name
        data = fetch_data_from_elasticsearch(
            index_name=os.getenv(
                "ELASTICSEARCH_EXCHANGERATES_INDEX_NAME", "exchangeratesapi"
            )
        )

        return {"message": "Data fetched successfully", "data": data}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}


@router.get("/weatherapi")
async def fetch_translate_store_weather_data():
    try:
        # Load the API configuration from environment variables
        api_url = os.getenv("WEATHER_API_URL")
        api_key = os.getenv("WEATHER_API_KEY")
        location = os.getenv("WEATHER_API_LOCATION")

        if not api_url or not api_key or not location:
            raise HTTPException(
                status_code=500, detail="Weather API configuration not provided"
            )

        # Fetch data from the Weather API
        params = {"key": api_key, "q": location}
        data = await fetch_data_from_api(api_url, params)

        # Parsing the received JSON data (you can customize this part based on the actual response structure)
        location_name = data["location"]["name"]
        temperature_c = data["current"]["temp_c"]
        weather_condition = data["current"]["condition"]["text"]

        # Create the index if it does not exist
        try:
            create_index_if_not_exists()
        except Exception as e:
            logger.error(f"Error creating Elasticsearch index: {str(e)}")

        # Storing the data in Elasticsearch
        index_name = os.getenv("ELASTICSEARCH_WEATHER_INDEX_NAME", "weatherapi")

        # Log the data to be stored
        logger.info(f"Storing weather data in Elasticsearch: {data}")

        # Use the Elasticsearch client to index the data
        es.index(index=index_name, body=data)

        logger.info("Weather data stored in Elasticsearch successfully")
        logger.info("Weather data fetched, translated, and stored successfully")
        return {
            "message": "Weather data fetched, translated, and stored successfully",
            "data": {
                "location_name": location_name,
                "temperature_c": temperature_c,
                "weather_condition": weather_condition,
            },
        }
    except HTTPException as e:
        raise e  # No need to modify the exception here
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/weatherapidata")
async def get_weather_data():
    try:
        # Fetch data from Elasticsearch with a dynamic index name
        data = fetch_data_from_elasticsearch(
            index_name=os.getenv("ELASTICSEARCH_WEATHER_API_INDEX_NAME", "weatherapi")
        )

        return {"message": "Weather data fetched successfully", "data": data}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

# backend/src/api/handlers/exchangerates_handler.py
import os

import httpx
from config.elasticsearch_config import (  # check_elasticsearch,
    create_index_if_not_exists,
    es,
    fetch_data_from_elasticsearch,
)
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from loguru import logger

load_dotenv()

# Load the Exchange Rates API key from the environment
EXCHANGERATES_API_KEY = os.getenv("EXCHANGERATES_API_KEY")

router = APIRouter()


@router.get("/exchangeratesapi")
async def fetch_translate_store_data():
    try:
        # Check Elasticsearch connection
        # check_elasticsearch()

        if not EXCHANGERATES_API_KEY:
            raise HTTPException(
                status_code=500, detail="Exchange Rates API key not provided"
            )

        # Fetch data from the Exchange Rates API
        api_url = "http://api.exchangeratesapi.io/v1/latest"
        params = {"access_key": EXCHANGERATES_API_KEY}

        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params=params)

            if response.status_code == 403:
                raise HTTPException(
                    status_code=403, detail="Unauthorized access to Exchange Rates API"
                )

            response.raise_for_status()

            data = response.json()

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
        # Fetch data from Elasticsearch
        data = fetch_data_from_elasticsearch()

        return {"message": "Data fetched successfully", "data": data}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

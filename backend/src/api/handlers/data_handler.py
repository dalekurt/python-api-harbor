# backend/src/api/handlers/data_handler.py
import os

import httpx
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


async def fetch_data_from_api(api_url, params):
    try:
        # Fetch data from the specified API
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params=params)

            if response.status_code == 401:
                raise httpx.HTTPStatusError(
                    response=response,
                    request=response.request,
                    message="Unauthorized access to API",
                )

            response.raise_for_status()

            data = response.json()

        return data
    except httpx.HTTPStatusError as e:
        raise  # Re-raise the exception to be caught in the calling function
    except Exception as e:
        logger.error(f"Error fetching data from API: {str(e)}")
        raise

# backend/src/api/config/elasticsearch_config.py
import time

from elasticsearch import Elasticsearch
from fastapi import HTTPException
from loguru import logger

es = Elasticsearch(["http://localhost:9200"])

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 3


def check_elasticsearch():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            if es.ping():
                logger.info("Connected to Elasticsearch")
                return
        except Exception as e:
            logger.warning(f"Failed to connect to Elasticsearch: {str(e)}")
            retries += 1
            if retries < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                logger.error("Failed to connect to Elasticsearch after retries")
                raise HTTPException(
                    status_code=500, detail="Failed to connect to Elasticsearch"
                )
    raise HTTPException(
        status_code=500,
        detail=f"Failed to connect to Elasticsearch after {MAX_RETRIES} retries",
    )


def create_index_if_not_exists():
    index_name = "exchangeratesapi"
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        logger.info(f"Index '{index_name}' created in Elasticsearch")


def fetch_data_from_elasticsearch():
    try:
        index_name = "exchangeratesapi"  # Replace with your actual index name

        # Search for all documents in the index
        response = es.search(index=index_name, body={"query": {"match_all": {}}})

        # Extract hits (actual data) from the response
        hits = response.get("hits", {}).get("hits", [])

        # Extract source data from hits
        data = [hit["_source"] for hit in hits]

        return data
    except Exception as e:
        logger.error(f"Error fetching data from Elasticsearch: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

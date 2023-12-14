# backend/src/api/config/elasticsearch_config.py
import os
import time

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from fastapi import HTTPException
from loguru import logger

# TODO:Use the ELASTICSEARCH_URL environment variable if available, otherwise default to "http://localhost:9200"
elasticsearch_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
es = Elasticsearch([elasticsearch_url])

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


def create_index_if_not_exists(index_name):
    try:
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name)
            logger.info(f"Index '{index_name}' created in Elasticsearch")
    except Exception as e:
        logger.error(f"Error creating index '{index_name}' in Elasticsearch: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def fetch_data_from_elasticsearch(index_name):
    try:
        # Search for all documents in the index
        response = es.search(index=index_name, body={"query": {"match_all": {}}})

        # Extract hits (actual data) from the response
        hits = response.get("hits", {}).get("hits", [])

        # Extract source data from hits
        data = [hit["_source"] for hit in hits]

        logger.info(
            f"Successfully fetched data from Elasticsearch for index: {index_name}"
        )
        return data
    except Exception as e:
        # Log error and raise HTTPException
        logger.error(
            f"Error fetching data from Elasticsearch for index {index_name}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")

# server/app/databases/elasticsearch.py

import time
from contextlib import asynccontextmanager

from app.config.elasticsearch_config import ElasticsearchConfig
from app.config.logger_config import logger
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, HTTPException

elasticsearch_config = ElasticsearchConfig()
es = None

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 3


@asynccontextmanager
async def lifespan(app: FastAPI):
    global es
    es = get_elasticsearch_client()
    try:
        yield
    finally:
        await es.close()


def get_elasticsearch_client() -> AsyncElasticsearch:
    global es
    if es is None or getattr(es.transport, "closed", True):
        es = AsyncElasticsearch(
            [elasticsearch_config.ELASTICSEARCH_URL],
            http_auth=(
                elasticsearch_config.ELASTICSEARCH_USERNAME,
                elasticsearch_config.ELASTICSEARCH_PASSWORD,
            ),
        )
    return es


def check_elasticsearch():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            client = get_elasticsearch_client()
            if client.ping():
                logger.info("Connected to Elasticsearch")
                return
        except Exception as e:
            logger.warning(f"Failed to connect to Elasticsearch: {str(e)}")
            retries += 1
            if retries < MAX_RETRIES:
                next_retry_time = time.time() + RETRY_DELAY_SECONDS
                logger.info(
                    f"Retrying in {RETRY_DELAY_SECONDS} seconds (next retry at {next_retry_time})"
                )
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


async def create_index_if_not_exists(index_name):
    try:
        client = get_elasticsearch_client()
        if not await client.indices.exists(index=index_name):
            await client.indices.create(index=index_name)
            logger.info(f"Index '{index_name}' created in Elasticsearch")
    except Exception as e:
        logger.error(f"Error creating index '{index_name}' in Elasticsearch: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def fetch_data_from_elasticsearch(index_name):
    try:
        client = get_elasticsearch_client()
        # Search for all documents in the index
        response = await client.search(
            index=index_name, body={"query": {"match_all": {}}}
        )

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


async def close_elasticsearch_client(app: FastAPI) -> None:
    if es:
        await es.close()


app = FastAPI(lifespan={"startup": lifespan, "shutdown": close_elasticsearch_client})

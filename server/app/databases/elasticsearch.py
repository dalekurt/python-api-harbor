# server/app/databases/elasticsearch.py
import asyncio
from contextlib import asynccontextmanager

from app.config.elasticsearch_config import ElasticsearchConfig
from app.config.logger_config import logger
from elasticsearch import AsyncElasticsearch, ConnectionError, TransportError
from fastapi import FastAPI, HTTPException
from tenacity import before_sleep_log, retry, stop_after_attempt, wait_fixed

elasticsearch_config = ElasticsearchConfig()
es = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global es
    es = await get_elasticsearch_client()
    try:
        yield
    finally:
        await es.close()


@retry(
    wait=wait_fixed(3),
    stop=stop_after_attempt(3),
    before_sleep=before_sleep_log(logger, logger.level("DEBUG")),
)
async def get_elasticsearch_client() -> AsyncElasticsearch:
    global es
    if es is None or getattr(es.transport, "closed", True):
        try:
            es = AsyncElasticsearch(
                [elasticsearch_config.ELASTICSEARCH_URL],
                http_auth=(
                    elasticsearch_config.ELASTICSEARCH_USERNAME,
                    elasticsearch_config.ELASTICSEARCH_PASSWORD,
                ),
            )
            if await es.ping():
                logger.info("Connected to Elasticsearch")
            else:
                raise ConnectionError("Failed to ping Elasticsearch")
        except ConnectionError as e:
            logger.error(
                f"Connection error with Elasticsearch at {elasticsearch_config.ELASTICSEARCH_URL}: {e}"
            )
            raise
        except TransportError as e:
            logger.error(f"Transport error with Elasticsearch: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while connecting to Elasticsearch: {e}")
            raise
    return es


async def create_index_if_not_exists(index_name):
    try:
        client = await get_elasticsearch_client()
        if not await client.indices.exists(index=index_name):
            await client.indices.create(index=index_name)
            logger.info(f"Index '{index_name}' created in Elasticsearch")
    except ElasticsearchException as e:
        error_message = (
            f"Error creating index '{index_name}' in Elasticsearch: {str(e)}"
        )
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        logger.error(f"Unexpected error while creating index in Elasticsearch: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def fetch_data_from_elasticsearch(index_name):
    try:
        client = await get_elasticsearch_client()
        response = await client.search(
            index=index_name, body={"query": {"match_all": {}}}
        )
        hits = response.get("hits", {}).get("hits", [])
        data = [hit["_source"] for hit in hits]
        logger.info(
            f"Successfully fetched data from Elasticsearch for index: {index_name}"
        )
        return data
    except ElasticsearchException as e:
        error_message = (
            f"Error fetching data from Elasticsearch for index {index_name}: {str(e)}"
        )
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        logger.error(f"Unexpected error while fetching data from Elasticsearch: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def close_elasticsearch_client(app: FastAPI) -> None:
    if es:
        await es.close()

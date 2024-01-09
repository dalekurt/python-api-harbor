# server/app/routes/api_routes.py
import redis
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from shared.clients.dragonflydb import get_redis
from shared.clients.elasticsearch import get_elasticsearch_client
from shared.clients.mongodb import get_mongo_client
from shared.clients.temporal_client import create_temporal_client

router = APIRouter()


@router.get("/ping")
def ping():
    logger.info("Ping request received")
    return {"message": "pong"}


@router.get("/dragonflydb")
async def read_root(redis: redis.Redis = Depends(get_redis)):
    return {"message": "Hello, DragonflyDB!"}


@router.get("/temporal")
async def temporal(temporal_client=Depends(create_temporal_client)):
    logger.info("Handling Temporal request")
    return {"message": "Hello, Temporal!"}


@router.get("/mongodb")
async def mongodb(mongo_client=Depends(get_mongo_client)):
    try:
        # Assuming you have a 'users' collection
        user_document = mongo_client["your_database"]["users"].find_one({})
        if user_document:
            logger.info("Handling MongoDB request")
            return {"message": "Hello, MongoDB!", "user": user_document}
        else:
            raise HTTPException(status_code=404, detail="No user found in MongoDB")
    except Exception as e:
        logger.error(f"Error handling MongoDB request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/elasticsearch")
async def elasticsearch(elasticsearch_client=Depends(get_elasticsearch_client)):
    try:
        return {"message": "Hello, Elasticsearch!"}
    except Exception as e:
        logger.error(f"Error interacting with Elasticsearch: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

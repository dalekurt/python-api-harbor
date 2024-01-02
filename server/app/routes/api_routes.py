# server/app/routes/api_route.py
import redis
from app.databases.dragonflydb import get_redis
from app.databases.mongodb import get_mongo_client
from app.databases.temporal_client import create_temporal_client
from fastapi import APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

router = APIRouter()

# CORS (Cross-Origin Resource Sharing) Middleware
# router.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@router.get("/ping")
def ping():
    logger.info("Ping request received")
    return {"message": "pong"}


@router.get("/dragonflydb")
async def read_root(redis: redis.Redis = Depends(get_redis)):
    return {"message": "Hello, DragonflyDB!"}


@router.get("/temporal")
async def temporal_example(temporal_client=Depends(create_temporal_client)):
    logger.info("Handling Temporal request")
    return {"message": "Hello, Temporal!"}


@router.get("/mongodb")
async def mongodb_example(mongo_client=Depends(get_mongo_client)):
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

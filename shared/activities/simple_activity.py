# shared/activities/simple_activity.py
from temporalio import activity

from shared.config.logger_config import logger


@activity.defn
async def simple_activity() -> str:
    logger.info("Simple activity executed")
    return "Activity result"

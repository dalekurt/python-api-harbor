# shared/config/dragonflydb_config.py
import os

from tenacity import retry, stop_after_attempt, wait_fixed

DRAGONFLYDB_CONFIG = {
    "host": os.getenv("DRAGONFLYDB_HOST", "localhost"),
    "port": int(os.getenv("DRAGONFLYDB_PORT", "6379")),
    "retry": {
        "wait": wait_fixed(1),
        "stop": stop_after_attempt(10),
    },
}

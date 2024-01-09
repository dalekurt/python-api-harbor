# server/app/config/temporal_config.py
import os

TEMPORAL_CONFIG = {
    "host": os.getenv("TEMPORAL_HOST", "localhost"),
    "port": int(os.getenv("TEMPORAL_PORT", "7233")),
}

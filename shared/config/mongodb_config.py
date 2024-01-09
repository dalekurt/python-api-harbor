# server/app/config/mongodb_config.py
import os

MONGODB_CONFIG = {
    "host": os.getenv("MONGODB_HOST", "localhost"),
    "port": int(os.getenv("MONGODB_PORT", 27017)),
    "database": os.getenv("MONGODB_DATABASE", "your_default_database"),
    "username": os.getenv("MONGODB_USERNAME", "your_username"),
    "password": os.getenv("MONGODB_PASSWORD", "your_password"),
    "auth_source": os.getenv("MONGODB_AUTH_SOURCE", "admin"),
}

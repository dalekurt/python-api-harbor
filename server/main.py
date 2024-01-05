# server/main.py
from app.config.app_config import configure_app
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

app = configure_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

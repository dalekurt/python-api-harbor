import os
import sys
from pathlib import Path

root_dir = Path(__file__).parent
sys.path.append(str(root_dir / "server"))

from server.main import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

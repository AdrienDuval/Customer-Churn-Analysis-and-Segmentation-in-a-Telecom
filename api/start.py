"""
Simple script to start the FastAPI server.
Run from FinalProject directory: python api/start.py
Or from api directory: python start.py
"""
import sys
from pathlib import Path

# Add parent directory to path
current_file = Path(__file__)
if current_file.name == "start.py":
    parent_dir = current_file.parent.parent
else:
    parent_dir = current_file.parent

if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Import and run
from api.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

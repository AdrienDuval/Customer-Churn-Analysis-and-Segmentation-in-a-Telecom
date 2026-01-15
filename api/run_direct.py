"""
Alternative script to run the FastAPI application by importing directly.

This version works when run from the FinalProject directory:
    python api/run_direct.py

Or from the api directory:
    cd api
    python run_direct.py
"""
import sys
from pathlib import Path

# Add parent directory to path
current_file = Path(__file__)
if current_file.name == "run_direct.py":
    # Running from api directory
    parent_dir = current_file.parent.parent
else:
    # Running from FinalProject directory
    parent_dir = current_file.parent

if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Now import and run
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

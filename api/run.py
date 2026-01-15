"""
Script to run the FastAPI application.

Can be run from either:
- FinalProject/api/ directory: python run.py
- FinalProject/ directory: python api/run.py
"""
import sys
from pathlib import Path
import uvicorn

if __name__ == "__main__":
    # Get the parent directory (FinalProject) and add it to Python path
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    
    # Add parent directory to Python path so 'api' module can be found
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info",
        reload_dirs=[str(parent_dir)]  # Watch parent directory for changes
    )

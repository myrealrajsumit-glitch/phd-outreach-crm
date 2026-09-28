import sys
import os
from pathlib import Path

# Add backend directory to sys.path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
BACKEND_DIR = ROOT_DIR / "backend"

for path_str in [str(BACKEND_DIR), str(ROOT_DIR)]:
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

# Declare Vercel environment
os.environ["VERCEL"] = "1"

# Import the FastAPI application
from app.main import app

# Vercel ASGI serverless handler
handler = app

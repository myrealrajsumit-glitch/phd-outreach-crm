import sys
import os
import traceback
from pathlib import Path

# Add backend directory and parent directories to sys.path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
BACKEND_DIR = ROOT_DIR / "backend"

for path_str in [str(BACKEND_DIR), str(ROOT_DIR), str(CURRENT_DIR)]:
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

os.environ["VERCEL"] = "1"

try:
    from app.main import app
    handler = app
except Exception as e:
    err_tb = traceback.format_exc()
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    app = FastAPI()
    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all(full_path: str):
        return JSONResponse(
            status_code=500, 
            content={
                "error": "Backend initialization failed",
                "detail": str(e),
                "traceback": err_tb
            }
        )
    handler = app

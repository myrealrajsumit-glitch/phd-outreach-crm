import os
import sys
from pathlib import Path
import uvicorn

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from app.config import settings

if __name__ == "__main__":
    port = int(getattr(settings, "BACKEND_PORT", getattr(settings, "PORT", 8000)))
    print(f"Starting PhD Outreach CRM backend on http://localhost:{port}...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)

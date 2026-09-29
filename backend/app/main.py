from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.api.api_router import api_router
from app.services.queue_service import queue_worker
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    if not os.environ.get("VERCEL"):
        await queue_worker.start()
    yield
    # Shutdown
    if not os.environ.get("VERCEL"):
        await queue_worker.stop()

app = FastAPI(
    title="PhD Professor Review & Cold Outreach CRM",
    description="Academic relationship management & Gemini-powered cold outreach intelligence.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for easy local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Direct routes without /api prefix (for Vercel rewrites that strip /api)
from app.api.auth_routes import router as auth_router
from app.api.professor_routes import router as professor_router
from app.api.email_routes import router as email_router
from app.api.ai_routes import router as ai_router
from app.api.stats_routes import router as stats_router
from app.api.discovery_routes import router as discovery_router

app.include_router(auth_router)
app.include_router(professor_router)
app.include_router(email_router)
app.include_router(ai_router)
app.include_router(stats_router)
app.include_router(discovery_router)

@app.get("/")
@app.get("/api")
@app.get("/api/")
async def api_root():
    return {
        "status": "online",
        "service": "PhD Professor Review & Cold Outreach CRM API",
        "runtime": "Vercel Serverless Python" if os.environ.get("VERCEL") else "FastAPI Uvicorn"
    }

@app.get("/health")
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "PhD Professor Review & Outreach CRM",
        "environment": settings.ENVIRONMENT,
        "runtime": "Vercel Serverless" if os.environ.get("VERCEL") else "Standard Server",
        "active_gemini_keys": len(settings.gemini_keys),
        "model": settings.GEMINI_MODEL
    }

# Serve frontend build in production / Hugging Face Spaces
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))

if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="API route not found")
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path, media_type="text/html")
        return {"detail": "Frontend build not found"}

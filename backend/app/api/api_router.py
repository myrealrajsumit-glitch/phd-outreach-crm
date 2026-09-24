from fastapi import APIRouter
from app.api.auth_routes import router as auth_router
from app.api.professor_routes import router as professor_router
from app.api.email_routes import router as email_router
from app.api.ai_routes import router as ai_router
from app.api.stats_routes import router as stats_router
from app.api.discovery_routes import router as discovery_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(professor_router)
api_router.include_router(email_router)
api_router.include_router(ai_router)
api_router.include_router(stats_router)
api_router.include_router(discovery_router)

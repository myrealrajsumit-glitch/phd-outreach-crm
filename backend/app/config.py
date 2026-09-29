import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings

# Determine project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

def resolve_database_url() -> str:
    env_db = (
        os.environ.get("DATABASE_URL")
        or os.environ.get("POSTGRES_URL")
        or os.environ.get("POSTGRES_PRISMA_URL")
        or os.environ.get("POSTGRES_URL_NON_POOLING")
        or os.environ.get("SUPABASE_DB_URL")
    )
    if env_db and env_db.strip():
        db_url = env_db.strip()
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+asyncpg://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return db_url

    if os.environ.get("VERCEL"):
        tmp_db = Path("/tmp/phd_crm.db")
        source_db = BASE_DIR / "phd_crm.db"
        if not tmp_db.exists() and source_db.exists():
            import shutil
            try:
                shutil.copyfile(source_db, tmp_db)
            except Exception as e:
                print(f"Notice: copying initial db to /tmp: {e}")
        return f"sqlite+aiosqlite:///{tmp_db.as_posix()}"
    return f"sqlite+aiosqlite:///{(BASE_DIR / 'phd_crm.db').as_posix()}"

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # Permanent Local Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 5555
    FRONTEND_PORT: int = 5566
    
    # Security & Auth
    SECRET_KEY: str = "phd_outreach_crm_super_secret_jwt_key_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Database - Absolute canonical path (uses /tmp on Vercel serverless)
    DATABASE_URL: str = resolve_database_url()
    
    # Gemini API Keys (Multi-Key Pool)
    GEMINI_API_KEY_01: str = ""
    GEMINI_API_KEY_02: str = ""
    GEMINI_API_KEY_03: str = ""
    GEMINI_API_KEY_04: str = ""
    GEMINI_API_KEY_05: str = ""
    GEMINI_API_KEY_06: str = ""
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.1-flash-lite"
    
    # OpenRouter API Key (fallback)
    OPENROUTER_API_KEY: str = ""
    
    # Dispatcher Limits
    MAX_EMAILS_PER_DAY: int = 25
    MIN_DELAY_BETWEEN_EMAILS_SECONDS: int = 45
    COOLDOWN_PERIOD_DAYS: int = 180
    
    # SMTP Outreach Defaults
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "Sumit Raj"
    SMTP_USE_TLS: bool = True

    class Config:
        env_file = str(ENV_FILE)
        extra = "allow"

    @property
    def gemini_keys(self) -> List[str]:
        """Return all non-empty Gemini keys in pool."""
        keys = []
        for i in range(1, 7):
            val = getattr(self, f"GEMINI_API_KEY_{i:02d}", "")
            if val and val.strip() and val not in keys:
                keys.append(val.strip())
        if self.GEMINI_API_KEY and self.GEMINI_API_KEY.strip() and self.GEMINI_API_KEY.strip() not in keys:
            keys.append(self.GEMINI_API_KEY.strip())
        return keys

settings = Settings()

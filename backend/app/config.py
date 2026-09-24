import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings

# Determine project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

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
    
    # Database - Absolute canonical path
    DATABASE_URL: str = f"sqlite+aiosqlite:///{(BASE_DIR / 'phd_crm.db').as_posix()}"
    
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

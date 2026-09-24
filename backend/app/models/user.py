from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    target_field = Column(String(255), nullable=True, default="Computer Science & AI")
    current_degree = Column(String(255), nullable=True, default="M.S. in Computer Science")
    research_interests = Column(Text, nullable=True)
    cv_summary = Column(Text, nullable=True)
    
    # SMTP Configuration for personal direct outreach
    smtp_host = Column(String(255), nullable=True)
    smtp_port = Column(Integer, nullable=True, default=587)
    smtp_user = Column(String(255), nullable=True)
    smtp_password = Column(String(255), nullable=True)  # App password
    smtp_from_name = Column(String(255), nullable=True)
    smtp_use_tls = Column(Boolean, default=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    professors = relationship("Professor", back_populates="user", cascade="all, delete-orphan")
    templates = relationship("EmailTemplate", back_populates="user", cascade="all, delete-orphan")

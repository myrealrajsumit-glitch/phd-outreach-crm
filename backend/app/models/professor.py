from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Professor(Base):
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    institution = Column(String(255), nullable=False, index=True)
    department = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True, default="Professor")
    homepage_url = Column(String(512), nullable=True)
    lab_url = Column(String(512), nullable=True)
    country = Column(String(100), nullable=True, default="USA")
    
    # Status in CRM Funnel:
    # 'Identified', 'Reviewing', 'Draft_Ready', 'Scheduled', 'Sent', 'Replied', 'Interview', 'Archived'
    status = Column(String(50), default="Identified", index=True)
    
    # Review details
    research_topics = Column(Text, nullable=True)  # Comma-separated or JSON list
    accepting_students = Column(String(50), default="Unknown")  # 'Yes', 'No', 'Grant_Funded', 'Unknown'
    match_score = Column(Float, default=0.0)  # 1.0 to 10.0 scale
    notes = Column(Text, nullable=True)
    ai_synthesis = Column(Text, nullable=True)  # Gemini generated paper critique & research angles

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="professors")
    papers = relationship("Paper", back_populates="professor", cascade="all, delete-orphan")
    emails = relationship("EmailDraft", back_populates="professor", cascade="all, delete-orphan")

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    professor_id = Column(Integer, ForeignKey("professors.id"), nullable=False)
    title = Column(String(512), nullable=False)
    year = Column(Integer, nullable=True)
    venue = Column(String(255), nullable=True)
    abstract = Column(Text, nullable=True)
    doi_or_url = Column(String(512), nullable=True)
    key_contributions = Column(Text, nullable=True)
    candidate_overlap_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    professor = relationship("Professor", back_populates="papers")

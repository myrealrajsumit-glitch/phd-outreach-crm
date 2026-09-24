from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PaperBase(BaseModel):
    title: str
    year: Optional[int] = None
    venue: Optional[str] = None
    abstract: Optional[str] = None
    doi_or_url: Optional[str] = None
    key_contributions: Optional[str] = None
    candidate_overlap_notes: Optional[str] = None

class PaperCreate(PaperBase):
    pass

class PaperResponse(PaperBase):
    id: int
    professor_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProfessorBase(BaseModel):
    name: str
    email: EmailStr
    institution: str
    department: Optional[str] = None
    title: Optional[str] = "Professor"
    homepage_url: Optional[str] = None
    lab_url: Optional[str] = None
    country: Optional[str] = "USA"
    status: Optional[str] = "Identified"
    research_topics: Optional[str] = None
    accepting_students: Optional[str] = "Unknown"
    match_score: Optional[float] = 0.0
    notes: Optional[str] = None
    ai_synthesis: Optional[str] = None

class ProfessorCreate(ProfessorBase):
    papers: Optional[List[PaperCreate]] = None

class ProfessorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    institution: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None
    homepage_url: Optional[str] = None
    lab_url: Optional[str] = None
    country: Optional[str] = None
    status: Optional[str] = None
    research_topics: Optional[str] = None
    accepting_students: Optional[str] = None
    match_score: Optional[float] = None
    notes: Optional[str] = None
    ai_synthesis: Optional[str] = None

class ProfessorResponse(ProfessorBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    papers: List[PaperResponse] = []

    class Config:
        from_attributes = True

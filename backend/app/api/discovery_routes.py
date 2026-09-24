from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from app.core.database import get_db
from app.api.auth_routes import get_current_user
from app.models.user import User
from app.models.professor import Professor, Paper
from app.schemas.professor import ProfessorResponse
from app.services.discovery_service import DiscoveryService

router = APIRouter(prefix="/discovery", tags=["Faculty Discovery"])

class ImportFacultyRequest(BaseModel):
    name: str
    email: Optional[str] = None
    institution: str
    department: Optional[str] = None
    title: Optional[str] = "Professor"
    country: Optional[str] = "USA"
    research_topics: Optional[str] = None
    accepting_students: Optional[str] = "Likely"
    notes: Optional[str] = None
    recent_paper: Optional[Dict[str, Any]] = None

@router.get("/search")
async def search_faculty(
    query: str = Query("Machine Learning", description="Research area, keyword, or professor name"),
    source: str = Query("all", description="'all', 'openalex', or 'nsf'"),
    country: Optional[str] = Query(None, description="Country filter, e.g., 'US', 'GB', 'CA'"),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items = await DiscoveryService.discover_faculty(
        query=query, 
        source=source, 
        country=country, 
        limit=limit
    )

    # Cross-reference with user's CRM database to check in_crm status
    user_profs_stmt = select(Professor.id, Professor.name, Professor.email).where(Professor.user_id == current_user.id)
    result = await db.execute(user_profs_stmt)
    existing_profs = result.all()
    
    existing_lookup = {}
    for pid, pname, pemail in existing_profs:
        existing_lookup[pname.lower().strip()] = pid
        if pemail:
            existing_lookup[pemail.lower().strip()] = pid

    for item in items:
        name_key = item["name"].lower().strip()
        email_key = item.get("email", "").lower().strip()
        if name_key in existing_lookup:
            item["in_crm"] = True
            item["crm_id"] = existing_lookup[name_key]
        elif email_key in existing_lookup:
            item["in_crm"] = True
            item["crm_id"] = existing_lookup[email_key]
        else:
            item["in_crm"] = False
            item["crm_id"] = None

    return {
        "query": query,
        "source": source,
        "country": country,
        "count": len(items),
        "results": items
    }

@router.post("/import", response_model=ProfessorResponse)
async def import_faculty_to_crm(
    req: ImportFacultyRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if professor with same name already exists for this user
    existing_stmt = select(Professor).where(
        Professor.user_id == current_user.id,
        Professor.name.ilike(req.name.strip())
    ).options(selectinload(Professor.papers))
    existing_res = await db.execute(existing_stmt)
    existing_prof = existing_res.scalar_one_or_none()

    if existing_prof:
        return existing_prof

    # Create new professor
    email_to_use = req.email or f"{req.name.lower().replace(' ', '.')}@university.edu"
    new_prof = Professor(
        user_id=current_user.id,
        name=req.name.strip(),
        email=email_to_use,
        institution=req.institution.strip(),
        department=req.department or "Department of Computer Science",
        title=req.title or "Professor",
        country=req.country or "USA",
        status="Identified",
        research_topics=req.research_topics or "Artificial Intelligence",
        accepting_students=req.accepting_students or "Likely",
        match_score=8.5,
        notes=req.notes or f"Discovered via Academic Outreach Discovery engine for research in: {req.research_topics or req.name}."
    )
    db.add(new_prof)
    await db.flush()

    # Add recent paper if available
    if req.recent_paper and req.recent_paper.get("title"):
        paper_obj = Paper(
            professor_id=new_prof.id,
            title=req.recent_paper.get("title"),
            year=req.recent_paper.get("year") or 2025,
            venue=req.recent_paper.get("venue") or "Academic Venue",
            abstract=req.recent_paper.get("abstract"),
            doi_or_url=req.recent_paper.get("doi_or_url")
        )
        db.add(paper_obj)

    await db.commit()

    # Reload with papers
    stmt = select(Professor).where(Professor.id == new_prof.id).options(selectinload(Professor.papers))
    res = await db.execute(stmt)
    return res.scalar_one()

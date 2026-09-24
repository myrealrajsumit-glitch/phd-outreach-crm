from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.core.database import get_db
from app.api.auth_routes import get_current_user
from app.models.user import User
from app.models.professor import Professor, Paper
from app.schemas.professor import (
    ProfessorCreate, ProfessorUpdate, ProfessorResponse,
    PaperCreate, PaperResponse
)

router = APIRouter(prefix="/professors", tags=["Professors"])

@router.get("", response_model=List[ProfessorResponse])
async def list_professors(
    search: Optional[str] = Query(None, description="Search by name, institution or topics"),
    status: Optional[str] = Query(None, description="Filter by pipeline status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = (
        select(Professor)
        .where(Professor.user_id == current_user.id)
        .options(selectinload(Professor.papers))
        .order_by(desc(Professor.updated_at))
    )

    if status and status != "All":
        query = query.where(Professor.status == status)

    if search:
        search_fmt = f"%{search}%"
        query = query.where(
            or_(
                Professor.name.ilike(search_fmt),
                Professor.institution.ilike(search_fmt),
                Professor.department.ilike(search_fmt),
                Professor.research_topics.ilike(search_fmt)
            )
        )

    result = await db.execute(query)
    return result.scalars().all()

@router.post("", response_model=ProfessorResponse)
async def create_professor(
    prof_data: ProfessorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_prof = Professor(
        user_id=current_user.id,
        name=prof_data.name,
        email=prof_data.email,
        institution=prof_data.institution,
        department=prof_data.department,
        title=prof_data.title,
        homepage_url=prof_data.homepage_url,
        lab_url=prof_data.lab_url,
        country=prof_data.country,
        status=prof_data.status or "Identified",
        research_topics=prof_data.research_topics,
        accepting_students=prof_data.accepting_students or "Unknown",
        match_score=prof_data.match_score or 0.0,
        notes=prof_data.notes,
        ai_synthesis=prof_data.ai_synthesis
    )
    db.add(new_prof)
    await db.flush()

    if prof_data.papers:
        for p in prof_data.papers:
            paper_obj = Paper(
                professor_id=new_prof.id,
                title=p.title,
                year=p.year,
                venue=p.venue,
                abstract=p.abstract,
                doi_or_url=p.doi_or_url,
                key_contributions=p.key_contributions,
                candidate_overlap_notes=p.candidate_overlap_notes
            )
            db.add(paper_obj)

    await db.commit()
    
    # Reload with papers
    stmt = select(Professor).where(Professor.id == new_prof.id).options(selectinload(Professor.papers))
    res = await db.execute(stmt)
    return res.scalar_one()

@router.get("/{prof_id}", response_model=ProfessorResponse)
async def get_professor(
    prof_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = (
        select(Professor)
        .where(Professor.id == prof_id, Professor.user_id == current_user.id)
        .options(selectinload(Professor.papers))
    )
    res = await db.execute(stmt)
    prof = res.scalar_one_or_none()
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")
    return prof

@router.put("/{prof_id}", response_model=ProfessorResponse)
async def update_professor(
    prof_id: int,
    updates: ProfessorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = (
        select(Professor)
        .where(Professor.id == prof_id, Professor.user_id == current_user.id)
        .options(selectinload(Professor.papers))
    )
    res = await db.execute(stmt)
    prof = res.scalar_one_or_none()
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")

    for field, val in updates.model_dump(exclude_unset=True).items():
        setattr(prof, field, val)

    await db.commit()
    await db.refresh(prof)
    return prof

@router.delete("/{prof_id}")
async def delete_professor(
    prof_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Professor).where(Professor.id == prof_id, Professor.user_id == current_user.id)
    res = await db.execute(stmt)
    prof = res.scalar_one_or_none()
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")

    await db.delete(prof)
    await db.commit()
    return {"success": True, "message": "Professor deleted successfully"}

@router.post("/{prof_id}/papers", response_model=PaperResponse)
async def add_paper_to_professor(
    prof_id: int,
    paper_data: PaperCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Professor).where(Professor.id == prof_id, Professor.user_id == current_user.id)
    res = await db.execute(stmt)
    prof = res.scalar_one_or_none()
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")

    paper = Paper(
        professor_id=prof.id,
        title=paper_data.title,
        year=paper_data.year,
        venue=paper_data.venue,
        abstract=paper_data.abstract,
        doi_or_url=paper_data.doi_or_url,
        key_contributions=paper_data.key_contributions,
        candidate_overlap_notes=paper_data.candidate_overlap_notes
    )
    db.add(paper)
    await db.commit()
    await db.refresh(paper)
    return paper

@router.delete("/papers/{paper_id}")
async def delete_paper(
    paper_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = (
        select(Paper)
        .join(Professor)
        .where(Paper.id == paper_id, Professor.user_id == current_user.id)
    )
    res = await db.execute(stmt)
    paper = res.scalar_one_or_none()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    await db.delete(paper)
    await db.commit()
    return {"success": True, "message": "Paper removed"}

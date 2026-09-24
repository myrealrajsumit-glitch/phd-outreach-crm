from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.api.auth_routes import get_current_user
from app.models.user import User
from app.models.professor import Professor
from app.schemas.ai import (
    AIReviewRequest, AIReviewResponse,
    AIEmailDraftRequest, AIEmailDraftResponse,
    AIFollowUpRequest, AIFollowUpResponse
)
from app.services.ai_service import ai_service

router = APIRouter(prefix="/ai", tags=["AI Intelligence"])

@router.post("/review", response_model=AIReviewResponse)
async def review_professor_research(
    req: AIReviewRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = (
        select(Professor)
        .where(Professor.id == req.professor_id, Professor.user_id == current_user.id)
        .options(selectinload(Professor.papers))
    )
    res = await db.execute(stmt)
    prof = res.scalar_one_or_none()
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")

    papers_data = [
        {
            "title": p.title,
            "year": p.year,
            "venue": p.venue,
            "abstract": p.abstract
        }
        for p in prof.papers
    ]

    try:
        review_result = ai_service.synthesize_professor_research(
            professor_name=prof.name,
            institution=prof.institution,
            topics=prof.research_topics or "General Computer Science / AI",
            papers=papers_data,
            candidate_field=current_user.target_field or "Computer Science",
            candidate_interests=current_user.research_interests or "Machine Learning, Systems"
        )
        
        # Save synthesis and match score to professor record
        prof.match_score = float(review_result.get("match_score", 7.0))
        prof.ai_synthesis = review_result.get("synthesis_markdown", "")
        if prof.status == "Identified":
            prof.status = "Reviewing"

        await db.commit()

        return AIReviewResponse(
            professor_id=prof.id,
            match_score=prof.match_score,
            key_findings=review_result.get("key_findings", []),
            research_gaps=review_result.get("research_gaps", []),
            discussion_questions=review_result.get("discussion_questions", []),
            synthesis_markdown=prof.ai_synthesis
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI synthesis failed: {str(e)}")

@router.post("/draft-email", response_model=AIEmailDraftResponse)
async def generate_email_draft(
    req: AIEmailDraftRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prof = None
    target_papers = []
    prof_name = req.professor_name
    institution = req.institution or "Academic Department"
    topics = req.research_topics or current_user.research_interests or current_user.target_field or "Computer Science & AI"

    if req.professor_id:
        stmt = (
            select(Professor)
            .where(Professor.id == req.professor_id, Professor.user_id == current_user.id)
            .options(selectinload(Professor.papers))
        )
        res = await db.execute(stmt)
        prof = res.scalar_one_or_none()

    # If no professor found by ID but recipient_email provided, try matching by email
    if not prof and req.recipient_email:
        stmt = (
            select(Professor)
            .where(Professor.email == req.recipient_email.strip(), Professor.user_id == current_user.id)
            .options(selectinload(Professor.papers))
        )
        res = await db.execute(stmt)
        prof = res.scalar_one_or_none()

    if prof:
        prof_name = prof.name
        institution = prof.institution
        topics = prof.research_topics or topics
        for p in prof.papers:
            if req.paper_ids:
                if p.id in req.paper_ids:
                    target_papers.append({"title": p.title, "year": p.year, "venue": p.venue, "abstract": p.abstract})
            else:
                target_papers.append({"title": p.title, "year": p.year, "venue": p.venue, "abstract": p.abstract})
    else:
        # Fallback intelligent extraction if no DB professor selected
        if not prof_name and req.recipient_email:
            username = req.recipient_email.split('@')[0]
            parts = [part.capitalize() for part in username.replace('.', ' ').replace('_', ' ').split() if part]
            prof_name = f"Prof. {' '.join(parts)}" if parts else "Professor"
            if '@' in req.recipient_email:
                domain = req.recipient_email.split('@')[1]
                institution = domain.replace('.edu', ' University').replace('.ac.uk', ' University').replace('.org', '').title()
        if not prof_name:
            prof_name = "Professor"

    try:
        draft_result = ai_service.draft_academic_cold_email(
            professor_name=prof_name,
            institution=institution,
            papers=target_papers,
            candidate_name=current_user.full_name or "PhD Applicant",
            candidate_degree=current_user.current_degree or "M.S. in Computer Science",
            candidate_interests=topics,
            candidate_cv_summary=current_user.cv_summary or "Proven track record in research and development.",
            tone=req.tone or "Formal Academic",
            word_count=req.word_count or 250,
            custom_instructions=req.custom_instructions
        )

        return AIEmailDraftResponse(
            subject=draft_result.get("subject", f"PhD Application Inquiry - {current_user.full_name}"),
            body=draft_result.get("body", ""),
            tone_used=draft_result.get("tone_used", req.tone or "Formal Academic"),
            grounded_citations=draft_result.get("grounded_citations", []),
            suggested_call_to_action=draft_result.get("suggested_call_to_action", "Request for a 15-minute video call")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI email drafting failed: {str(e)}")

@router.post("/follow-up", response_model=AIFollowUpResponse)
async def generate_follow_up_email(
    req: AIFollowUpRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prof_name = req.professor_name or "Professor"
    institution = req.institution or "Academic Department"
    prev_subject = req.previous_subject or f"PhD Inquiry - {current_user.target_field or 'Research Position'}"
    prev_body = req.previous_body or "Initial inquiry regarding PhD openings and research alignment."

    if req.professor_id:
        stmt = (
            select(Professor)
            .where(Professor.id == req.professor_id, Professor.user_id == current_user.id)
        )
        res = await db.execute(stmt)
        prof = res.scalar_one_or_none()
        if prof:
            prof_name = prof.name
            institution = prof.institution

            from app.models.email import EmailDraft
            prev_draft = None
            if req.draft_id:
                prev_res = await db.execute(select(EmailDraft).where(EmailDraft.id == req.draft_id))
                prev_draft = prev_res.scalar_one_or_none()
            else:
                prev_res = await db.execute(
                    select(EmailDraft)
                    .where(EmailDraft.professor_id == prof.id)
                    .order_by(EmailDraft.updated_at.desc())
                    .limit(1)
                )
                prev_draft = prev_res.scalar_one_or_none()

            if prev_draft:
                prev_subject = prev_draft.subject
                prev_body = prev_draft.body

    try:
        fu_result = ai_service.draft_follow_up_email(
            professor_name=prof_name,
            institution=institution,
            previous_subject=prev_subject,
            previous_body=prev_body,
            candidate_name=current_user.full_name or "PhD Applicant",
            follow_up_stage=req.follow_up_stage or 1,
            custom_hook=req.custom_hook
        )
        return AIFollowUpResponse(
            subject=fu_result.get("subject", f"Re: {prev_subject}"),
            body=fu_result.get("body", ""),
            stage=fu_result.get("stage", req.follow_up_stage or 1)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI follow-up generation failed: {str(e)}")


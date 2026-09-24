from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from app.core.database import get_db
from app.api.auth_routes import get_current_user
from app.models.user import User
from app.models.professor import Professor
from app.models.email import EmailDraft, EmailTemplate
from app.models.queue import QueueItem
from app.schemas.email import (
    EmailDraftCreate, EmailDraftUpdate, EmailDraftResponse,
    TemplateCreate, TemplateResponse, SendEmailRequest, BatchSendRequest
)
from app.services.mail_service import mail_service

router = APIRouter(prefix="/emails", tags=["Emails"])

@router.get("", response_model=List[EmailDraftResponse])
async def list_email_drafts(
    professor_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = (
        select(EmailDraft)
        .join(Professor)
        .where(Professor.user_id == current_user.id)
        .order_by(desc(EmailDraft.updated_at))
    )
    if professor_id:
        query = query.where(EmailDraft.professor_id == professor_id)
    if status and status != "All":
        query = query.where(EmailDraft.status == status)

    res = await db.execute(query)
    return res.scalars().all()

@router.post("", response_model=EmailDraftResponse)
async def create_email_draft(
    draft_data: EmailDraftCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prof = None
    if draft_data.professor_id:
        stmt = select(Professor).where(Professor.id == draft_data.professor_id, Professor.user_id == current_user.id)
        res = await db.execute(stmt)
        prof = res.scalar_one_or_none()

    if not prof and draft_data.recipient_email:
        clean_email = draft_data.recipient_email.strip().lower()
        stmt = select(Professor).where(Professor.email == clean_email, Professor.user_id == current_user.id)
        res = await db.execute(stmt)
        prof = res.scalar_one_or_none()

        if not prof:
            username = clean_email.split('@')[0]
            parts = [part.capitalize() for part in username.replace('.', ' ').replace('_', ' ').split() if part]
            name = draft_data.recipient_name or (f"Prof. {' '.join(parts)}" if parts else "Faculty Member")
            inst = draft_data.institution or "Academic Department"
            if '@' in clean_email:
                domain = clean_email.split('@')[1]
                inst = domain.replace('.edu', ' University').replace('.ac.uk', ' University').replace('.org', '').title()

            prof = Professor(
                user_id=current_user.id,
                name=name,
                email=clean_email,
                institution=inst,
                status="Identified"
            )
            db.add(prof)
            await db.commit()
            await db.refresh(prof)

    if not prof:
        raise HTTPException(status_code=400, detail="Recipient professor ID or email address must be provided.")

    new_draft = EmailDraft(
        professor_id=prof.id,
        subject=draft_data.subject,
        body=draft_data.body,
        status="Draft"
    )
    db.add(new_draft)
    
    # Update professor status to Draft_Ready if currently Identified/Reviewing
    if prof.status in ["Identified", "Reviewing"]:
        prof.status = "Draft_Ready"

    await db.commit()
    await db.refresh(new_draft)
    return new_draft

@router.get("/templates", response_model=List[TemplateResponse])
async def list_templates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(EmailTemplate).where(EmailTemplate.user_id == current_user.id)
    res = await db.execute(stmt)
    templates = res.scalars().all()
    
    # If no templates exist, seed default academic templates
    if not templates:
        default_1 = EmailTemplate(
            user_id=current_user.id,
            name="Formal PhD Inquiry (Paper Grounded)",
            description="Polite, scholarly inquiry highlighting mutual alignment and citing recent publication.",
            subject_template="Prospective PhD Inquiry - {{research_topic}} - {{candidate_name}}",
            body_template="Dear Professor {{professor_last_name}},\n\nI hope you are having a productive semester.\n\nMy name is {{candidate_name}}, and I hold a {{candidate_degree}} specializing in {{candidate_field}}. I have been following your lab's recent contributions in {{research_topic}}, particularly your paper '{{paper_title}}'. Your methodology regarding {{key_takeaway}} strongly aligns with my previous research in {{candidate_experience}}.\n\nI am writing to inquire if you are accepting new PhD students into your group for the upcoming academic cycle. I would welcome the opportunity to discuss potential alignment or questions regarding your ongoing projects.\n\nI have attached my CV for your review. Would you be open to a brief 15-minute introductory video call at your convenience?\n\nThank you for your time and consideration.\n\nSincerely,\n{{candidate_name}}\n{{candidate_email}}",
            is_default=True
        )
        default_2 = EmailTemplate(
            user_id=current_user.id,
            name="Concise Direct Inquiry",
            description="Brief, punchy inquiry suitable for busy department chairs and high-volume PIs.",
            subject_template="Inquiry regarding PhD Openings in {{research_topic}} ({{candidate_name}})",
            body_template="Dear Professor {{professor_last_name}},\n\nI am writing to inquire about open PhD student positions in your laboratory at {{institution}} for the upcoming intake.\n\nI completed my {{candidate_degree}} with a focus on {{candidate_field}}. Having studied your paper on '{{paper_title}}', I am eager to contribute to your group's work on {{research_topic}}.\n\nMy CV is attached. If you are taking on students, I would greatly appreciate a brief opportunity to discuss how my background fits your team's goals.\n\nBest regards,\n{{candidate_name}}",
            is_default=False
        )
        db.add(default_1)
        db.add(default_2)
        await db.commit()
        
        res = await db.execute(stmt)
        templates = res.scalars().all()

    return templates

@router.post("/templates", response_model=TemplateResponse)
async def create_template(
    template_data: TemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_tpl = EmailTemplate(
        user_id=current_user.id,
        name=template_data.name,
        description=template_data.description,
        subject_template=template_data.subject_template,
        body_template=template_data.body_template,
        is_default=template_data.is_default or False
    )
    db.add(new_tpl)
    await db.commit()
    await db.refresh(new_tpl)
    return new_tpl

@router.get("/{draft_id}", response_model=EmailDraftResponse)
async def get_email_draft(
    draft_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(EmailDraft).join(Professor).where(EmailDraft.id == draft_id, Professor.user_id == current_user.id)
    res = await db.execute(stmt)
    draft = res.scalar_one_or_none()
    if not draft:
        raise HTTPException(status_code=404, detail="Email draft not found")
    return draft

@router.put("/{draft_id}", response_model=EmailDraftResponse)
async def update_email_draft(
    draft_id: int,
    updates: EmailDraftUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(EmailDraft).join(Professor).where(EmailDraft.id == draft_id, Professor.user_id == current_user.id)
    res = await db.execute(stmt)
    draft = res.scalar_one_or_none()
    if not draft:
        raise HTTPException(status_code=404, detail="Email draft not found")

    for field, val in updates.model_dump(exclude_unset=True).items():
        setattr(draft, field, val)

    await db.commit()
    await db.refresh(draft)
    return draft

@router.delete("/{draft_id}")
async def delete_email_draft(
    draft_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(EmailDraft).join(Professor).where(EmailDraft.id == draft_id, Professor.user_id == current_user.id)
    res = await db.execute(stmt)
    draft = res.scalar_one_or_none()
    if not draft:
        raise HTTPException(status_code=404, detail="Email draft not found")

    await db.delete(draft)
    await db.commit()
    return {"success": True, "message": "Draft deleted"}

@router.post("/send")
async def send_email_draft(
    req: SendEmailRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = (
        select(EmailDraft)
        .join(Professor)
        .where(EmailDraft.id == req.draft_id, Professor.user_id == current_user.id)
    )
    res = await db.execute(stmt)
    draft = res.scalar_one_or_none()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    # Load professor
    prof_stmt = select(Professor).where(Professor.id == draft.professor_id)
    prof_res = await db.execute(prof_stmt)
    professor = prof_res.scalar_one()

    if req.send_now:
        # Immediate send
        success, err = await mail_service.send_email(
            user=current_user,
            recipient_email=professor.email,
            subject=draft.subject,
            body=draft.body
        )
        if success:
            draft.status = "Sent"
            draft.sent_at = datetime.now(timezone.utc)
            professor.status = "Sent"
            await db.commit()
            return {"success": True, "status": "Sent", "message": f"Email dispatched to {professor.name} ({professor.email})"}
        else:
            draft.status = "Failed"
            draft.error_message = err
            await db.commit()
            raise HTTPException(status_code=500, detail=f"Failed to dispatch email: {err}")
    else:
        # Queue for scheduled dispatch
        scheduled_time = req.scheduled_for or (datetime.now(timezone.utc) + timedelta(minutes=5))
        draft.status = "Scheduled"
        draft.scheduled_for = scheduled_time
        professor.status = "Scheduled"

        queue_item = QueueItem(
            email_draft_id=draft.id,
            status="Queued",
            scheduled_for=scheduled_time
        )
        db.add(queue_item)
        await db.commit()
        return {"success": True, "status": "Scheduled", "message": f"Email scheduled for {scheduled_time.isoformat()}"}

@router.post("/batch-send")
async def batch_send_drafts(
    req: BatchSendRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not req.draft_ids:
        raise HTTPException(status_code=400, detail="No draft IDs provided.")

    queued_count = 0
    now = datetime.now(timezone.utc)

    for i, draft_id in enumerate(req.draft_ids):
        stmt = (
            select(EmailDraft)
            .join(Professor)
            .where(EmailDraft.id == draft_id, Professor.user_id == current_user.id)
        )
        res = await db.execute(stmt)
        draft = res.scalar_one_or_none()
        if not draft:
            continue

        scheduled_time = now + timedelta(seconds=i * req.interval_seconds)
        draft.status = "Scheduled"
        draft.scheduled_for = scheduled_time

        # Update professor
        prof_stmt = select(Professor).where(Professor.id == draft.professor_id)
        p_res = await db.execute(prof_stmt)
        prof = p_res.scalar_one()
        prof.status = "Scheduled"

        queue_item = QueueItem(
            email_draft_id=draft.id,
            status="Queued",
            scheduled_for=scheduled_time
        )
        db.add(queue_item)
        queued_count += 1

    await db.commit()
    return {
        "success": True,
        "queued_count": queued_count,
        "message": f"Successfully queued {queued_count} emails with {req.interval_seconds}s staggering."
    }


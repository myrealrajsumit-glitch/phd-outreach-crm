from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timezone
from app.core.database import get_db
from app.api.auth_routes import get_current_user
from app.models.user import User
from app.models.professor import Professor
from app.models.email import EmailDraft
from app.config import settings

router = APIRouter(prefix="/stats", tags=["Dashboard Statistics"])

@router.get("/dashboard")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Total professors
    prof_count_stmt = select(func.count(Professor.id)).where(Professor.user_id == current_user.id)
    total_professors = (await db.execute(prof_count_stmt)).scalar() or 0

    # Counts by status
    status_stmt = (
        select(Professor.status, func.count(Professor.id))
        .where(Professor.user_id == current_user.id)
        .group_by(Professor.status)
    )
    status_results = (await db.execute(status_stmt)).all()
    stage_counts = {status: count for status, count in status_results}

    # Email metrics
    total_drafts_stmt = (
        select(func.count(EmailDraft.id))
        .join(Professor)
        .where(Professor.user_id == current_user.id, EmailDraft.status == "Draft")
    )
    total_drafts = (await db.execute(total_drafts_stmt)).scalar() or 0

    total_sent_stmt = (
        select(func.count(EmailDraft.id))
        .join(Professor)
        .where(Professor.user_id == current_user.id, EmailDraft.status == "Sent")
    )
    total_sent = (await db.execute(total_sent_stmt)).scalar() or 0

    total_replied_stmt = (
        select(func.count(EmailDraft.id))
        .join(Professor)
        .where(Professor.user_id == current_user.id, EmailDraft.status == "Replied")
    )
    total_replied = (await db.execute(total_replied_stmt)).scalar() or 0

    # Scheduled in queue
    scheduled_stmt = (
        select(func.count(EmailDraft.id))
        .join(Professor)
        .where(Professor.user_id == current_user.id, EmailDraft.status == "Scheduled")
    )
    total_scheduled = (await db.execute(scheduled_stmt)).scalar() or 0

    reply_rate = round((total_replied / total_sent * 100), 1) if total_sent > 0 else 0.0

    # Recent professors
    recent_stmt = (
        select(Professor)
        .where(Professor.user_id == current_user.id)
        .order_by(Professor.updated_at.desc())
        .limit(5)
    )
    recent_profs = (await db.execute(recent_stmt)).scalars().all()

    return {
        "overview": {
            "total_professors": total_professors,
            "total_drafts": total_drafts,
            "total_sent": total_sent,
            "total_scheduled": total_scheduled,
            "total_replied": total_replied,
            "reply_rate_percent": reply_rate,
            "daily_velocity_limit": settings.MAX_EMAILS_PER_DAY
        },
        "funnel": {
            "Identified": stage_counts.get("Identified", 0),
            "Reviewing": stage_counts.get("Reviewing", 0),
            "Draft_Ready": stage_counts.get("Draft_Ready", 0),
            "Scheduled": stage_counts.get("Scheduled", 0),
            "Sent": stage_counts.get("Sent", 0),
            "Replied": stage_counts.get("Replied", 0),
            "Interview": stage_counts.get("Interview", 0),
            "Archived": stage_counts.get("Archived", 0)
        },
        "recent_activity": [
            {
                "id": p.id,
                "name": p.name,
                "institution": p.institution,
                "status": p.status,
                "match_score": p.match_score,
                "updated_at": p.updated_at
            }
            for p in recent_profs
        ]
    }

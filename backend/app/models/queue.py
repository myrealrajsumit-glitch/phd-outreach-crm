from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class QueueItem(Base):
    __tablename__ = "outreach_queue"

    id = Column(Integer, primary_key=True, index=True)
    email_draft_id = Column(Integer, ForeignKey("email_drafts.id"), nullable=False, unique=True)
    
    # Queue status: 'Queued', 'Processing', 'Sent', 'Failed', 'Cancelled'
    status = Column(String(50), default="Queued", index=True)
    scheduled_for = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    last_error = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    executed_at = Column(DateTime, nullable=True)

    email_draft = relationship("EmailDraft", back_populates="queue_item")

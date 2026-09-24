from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class EmailDraft(Base):
    __tablename__ = "email_drafts"

    id = Column(Integer, primary_key=True, index=True)
    professor_id = Column(Integer, ForeignKey("professors.id"), nullable=False)
    subject = Column(String(512), nullable=False)
    body = Column(Text, nullable=False)
    
    # Draft status: 'Draft', 'Scheduled', 'Sending', 'Sent', 'Failed', 'Replied'
    status = Column(String(50), default="Draft", index=True)
    
    sent_at = Column(DateTime, nullable=True)
    scheduled_for = Column(DateTime, nullable=True)
    
    # Reply tracking
    replied_at = Column(DateTime, nullable=True)
    reply_category = Column(String(50), nullable=True)  # 'Positive', 'Neutral', 'Not_Accepting', 'Referred'
    reply_summary = Column(Text, nullable=True)
    
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    professor = relationship("Professor", back_populates="emails")
    queue_item = relationship("QueueItem", back_populates="email_draft", uselist=False, cascade="all, delete-orphan")

class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=True)
    subject_template = Column(String(512), nullable=False)
    body_template = Column(Text, nullable=False)
    is_default = Column(Boolean, default=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="templates")

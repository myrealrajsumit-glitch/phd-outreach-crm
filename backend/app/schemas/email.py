from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

class EmailDraftBase(BaseModel):
    subject: str
    body: str

class EmailDraftCreate(EmailDraftBase):
    professor_id: Optional[int] = None
    recipient_email: Optional[str] = None
    recipient_name: Optional[str] = None
    institution: Optional[str] = None
    status: Optional[str] = "Draft"

class EmailDraftUpdate(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    status: Optional[str] = None
    reply_category: Optional[str] = None
    reply_summary: Optional[str] = None

class EmailDraftResponse(EmailDraftBase):
    id: int
    professor_id: int
    status: str
    sent_at: Optional[datetime] = None
    scheduled_for: Optional[datetime] = None
    replied_at: Optional[datetime] = None
    reply_category: Optional[str] = None
    reply_summary: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    subject_template: str
    body_template: str
    is_default: Optional[bool] = False

class TemplateCreate(TemplateBase):
    pass

class TemplateResponse(TemplateBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SendEmailRequest(BaseModel):
    draft_id: int
    send_now: bool = True
    scheduled_for: Optional[datetime] = None

class BatchSendRequest(BaseModel):
    draft_ids: list[int]
    interval_seconds: int = 60
    start_immediately: bool = True

class ScheduleAnalysisRequest(BaseModel):
    email: str
    institution: Optional[str] = None

class ScheduleAnalysisResponse(BaseModel):
    country: str
    city: str
    timezone: str
    matched_by: str
    diff_hours_str: str
    activity_state: str
    current_local_time: str
    current_ist_time: str
    optimal_slot_local: str
    optimal_slot_ist: str
    scheduled_iso: str
    scheduled_utc: str
    reasoning: List[str]
    friday_protected: bool

class SpamCheckRequest(BaseModel):
    subject: str
    body: str
    recipient_name: Optional[str] = None
    recipient_email: Optional[str] = None

class SpamCheckResponse(BaseModel):
    deliverability_score: int
    rating: str
    badge: str
    color: str
    word_count: int
    flags: List[str]
    suggestions: List[str]
    positive_signals: List[str]
    is_safe_to_send: bool

from pydantic import BaseModel
from typing import Optional, List

class AIReviewRequest(BaseModel):
    professor_id: int
    focus_topic: Optional[str] = None

class AIReviewResponse(BaseModel):
    professor_id: int
    match_score: float
    key_findings: List[str]
    research_gaps: List[str]
    discussion_questions: List[str]
    synthesis_markdown: str

class AIEmailDraftRequest(BaseModel):
    professor_id: int
    paper_ids: Optional[List[int]] = None
    tone: Optional[str] = "Formal Academic"  # 'Formal Academic', 'Direct & Concise', 'Technical Deep-Dive'
    word_count: Optional[int] = 250  # 150, 250, 350
    custom_instructions: Optional[str] = None

class AIEmailDraftResponse(BaseModel):
    subject: str
    body: str
    tone_used: str
    grounded_citations: List[str]
    suggested_call_to_action: str

class AIFollowUpRequest(BaseModel):
    professor_id: int
    draft_id: Optional[int] = None
    follow_up_stage: Optional[int] = 1  # 1 = 7 days, 2 = 14 days, 3 = final
    custom_hook: Optional[str] = None

class AIFollowUpResponse(BaseModel):
    subject: str
    body: str
    stage: int

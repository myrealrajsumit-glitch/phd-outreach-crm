from app.core.database import Base
from app.models.user import User
from app.models.professor import Professor, Paper
from app.models.email import EmailDraft, EmailTemplate
from app.models.queue import QueueItem

__all__ = ["Base", "User", "Professor", "Paper", "EmailDraft", "EmailTemplate", "QueueItem"]

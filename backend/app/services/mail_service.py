import aiosmtplib
from email.message import EmailMessage
import logging
from typing import Optional, Tuple
from app.models.user import User
from app.config import settings

logger = logging.getLogger(__name__)

class MailService:
    async def send_email(
        self,
        user: User,
        recipient_email: str,
        subject: str,
        body: str
    ) -> Tuple[bool, Optional[str]]:
        smtp_host = user.smtp_host or settings.SMTP_HOST
        smtp_port = user.smtp_port or settings.SMTP_PORT or 587
        smtp_user = user.smtp_user or settings.SMTP_USER or user.email
        smtp_password = user.smtp_password or settings.SMTP_PASSWORD
        smtp_from_name = user.smtp_from_name or settings.SMTP_FROM_NAME or user.full_name
        smtp_use_tls = user.smtp_use_tls if user.smtp_use_tls is not None else settings.SMTP_USE_TLS

        if not smtp_host or not smtp_user or not smtp_password:
            msg = "SMTP is not configured in Settings. Please enter your Gmail/University SMTP credentials (e.g. Gmail App Password) in Settings, or use 'Open in Gmail Web (1-Click)'."
            logger.warning(f"[SMTP UNCONFIGURED] Cannot send live email to {recipient_email}: {msg}")
            return False, msg

        try:
            message = EmailMessage()
            message["From"] = f"{smtp_from_name} <{smtp_user}>"
            message["To"] = recipient_email
            message["Subject"] = subject
            message.set_content(body)

            await aiosmtplib.send(
                message,
                hostname=smtp_host,
                port=smtp_port,
                username=smtp_user,
                password=smtp_password,
                start_tls=smtp_use_tls
            )
            logger.info(f"Email successfully sent to {recipient_email}")
            return True, None
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            return False, str(e)

mail_service = MailService()

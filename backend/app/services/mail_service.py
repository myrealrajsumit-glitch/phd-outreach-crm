import aiosmtplib
from email.message import EmailMessage
import logging
from typing import Optional, Tuple
from app.models.user import User

logger = logging.getLogger(__name__)

class MailService:
    async def send_email(
        self,
        user: User,
        recipient_email: str,
        subject: str,
        body: str
    ) -> Tuple[bool, Optional[str]]:
        if not user.smtp_host or not user.smtp_user or not user.smtp_password:
            msg = "SMTP is not configured in Settings. Please enter your Gmail/University SMTP credentials (e.g. Gmail App Password) in Settings, or use 'Open in Gmail Web (1-Click)'."
            logger.warning(f"[SMTP UNCONFIGURED] Cannot send live email to {recipient_email}: {msg}")
            return False, msg

        try:
            message = EmailMessage()
            from_name = user.smtp_from_name or user.full_name
            message["From"] = f"{from_name} <{user.smtp_user}>"
            message["To"] = recipient_email
            message["Subject"] = subject
            message.set_content(body)

            await aiosmtplib.send(
                message,
                hostname=user.smtp_host,
                port=user.smtp_port or 587,
                username=user.smtp_user,
                password=user.smtp_password,
                start_tls=user.smtp_use_tls
            )
            logger.info(f"Email successfully sent to {recipient_email}")
            return True, None
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            return False, str(e)

mail_service = MailService()

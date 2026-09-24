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
        """
        Dispatches an email. If the user hasn't configured SMTP credentials yet,
        it logs the email safely and returns simulated success to allow local testing.
        """
        if not user.smtp_host or not user.smtp_user or not user.smtp_password:
            logger.info(f"[SIMULATED OUTREACH] To: {recipient_email} | Subject: {subject} (Configure SMTP in settings for live dispatch)")
            return True, "Simulated dispatch (SMTP not configured in user settings)"

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

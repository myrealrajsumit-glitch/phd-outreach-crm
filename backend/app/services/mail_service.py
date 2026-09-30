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
            message["To"] = recipient_email.strip()
            message["Subject"] = subject
            message.set_content(body)

            # In SMTP: Port 465 uses direct SSL (use_tls=True, start_tls=False)
            # Port 587 uses STARTTLS (use_tls=False, start_tls=True)
            use_ssl = int(smtp_port) == 465
            use_starttls = (int(smtp_port) == 587) or (bool(smtp_use_tls) and not use_ssl)

            await aiosmtplib.send(
                message,
                hostname=smtp_host,
                port=int(smtp_port),
                username=smtp_user.strip(),
                password=smtp_password.strip(),
                use_tls=use_ssl,
                start_tls=use_starttls,
                timeout=12
            )
            logger.info(f"Email successfully sent to {recipient_email}")
            return True, None
        except aiosmtplib.errors.SMTPAuthenticationError as e:
            err_msg = f"SMTP Authentication Failed: Username or App Password rejected by {smtp_host}. Please verify your Gmail 16-character App Password in Settings."
            logger.error(f"{err_msg} - {e}")
            return False, err_msg
        except aiosmtplib.errors.SMTPServerDisconnected as e:
            err_msg = f"SMTP Server Disconnected: Connection closed unexpectedly by {smtp_host} on port {smtp_port}."
            logger.error(f"{err_msg} - {e}")
            return False, err_msg
        except aiosmtplib.errors.SMTPConnectError as e:
            err_msg = f"SMTP Connection Failed: Unable to connect to {smtp_host} on port {smtp_port}. Details: {e}"
            logger.error(err_msg)
            return False, err_msg
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            return False, str(e)

mail_service = MailService()

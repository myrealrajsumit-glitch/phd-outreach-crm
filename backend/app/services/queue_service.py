import asyncio
import logging
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import AsyncSessionLocal
from app.models.queue import QueueItem
from app.models.email import EmailDraft
from app.models.professor import Professor
from app.models.user import User
from app.services.mail_service import mail_service

logger = logging.getLogger(__name__)

class QueueWorker:
    def __init__(self):
        self.is_running = False
        self._task = None

    async def start(self):
        if not self.is_running:
            self.is_running = True
            self._task = asyncio.create_task(self._process_queue_loop())
            logger.info("Outreach Queue Worker started.")

    async def stop(self):
        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            logger.info("Outreach Queue Worker stopped.")

    async def _process_queue_loop(self):
        while self.is_running:
            try:
                await self.process_pending_items()
            except Exception as e:
                logger.error(f"Error in queue loop: {e}")
            await asyncio.sleep(10)  # Check queue every 10 seconds

    async def process_pending_items(self):
        now = datetime.now(timezone.utc)
        async with AsyncSessionLocal() as session:
            stmt = (
                select(QueueItem)
                .where(QueueItem.status == "Queued", QueueItem.scheduled_for <= now)
                .order_by(QueueItem.scheduled_for.asc())
                .limit(5)
            )
            result = await session.execute(stmt)
            items = result.scalars().all()

            for item in items:
                # Load email draft with professor and user
                draft_stmt = (
                    select(EmailDraft)
                    .where(EmailDraft.id == item.email_draft_id)
                    .options(selectinload(EmailDraft.professor).selectinload(Professor.user))
                )
                draft_res = await session.execute(draft_stmt)
                draft = draft_res.scalar_one_or_none()

                if not draft or not draft.professor or not draft.professor.user:
                    item.status = "Failed"
                    item.last_error = "Associated draft, professor, or user missing."
                    await session.commit()
                    continue

                item.status = "Processing"
                item.attempts += 1
                await session.commit()

                success, err = await mail_service.send_email(
                    user=draft.professor.user,
                    recipient_email=draft.professor.email,
                    subject=draft.subject,
                    body=draft.body
                )

                if success:
                    item.status = "Sent"
                    item.executed_at = datetime.now(timezone.utc)
                    draft.status = "Sent"
                    draft.sent_at = item.executed_at
                    draft.professor.status = "Sent"
                else:
                    if item.attempts >= item.max_attempts:
                        item.status = "Failed"
                        item.last_error = err
                        draft.status = "Failed"
                        draft.error_message = err
                    else:
                        item.status = "Queued"  # Will retry next loop
                        item.last_error = err

                await session.commit()

queue_worker = QueueWorker()

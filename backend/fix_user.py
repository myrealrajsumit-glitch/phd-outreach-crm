import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.professor import Professor
from app.models.user import User
from sqlalchemy import select, update

async def main():
    async with AsyncSessionLocal() as session:
        u_res = await session.execute(select(User).order_by(User.id.asc()).limit(1))
        user = u_res.scalar_one_or_none()
        if user:
            await session.execute(update(Professor).values(user_id=user.id))
            await session.commit()
            profs = (await session.execute(select(Professor))).scalars().all()
            print(f"Updated {len(profs)} professors to belong to user ID {user.id} ({user.full_name})")

if __name__ == "__main__":
    asyncio.run(main())

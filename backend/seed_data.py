import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.core.database import init_db, AsyncSessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.professor import Professor, Paper
from app.models.email import EmailDraft
from sqlalchemy import select

SEED_PROFESSORS = [
    {
        "name": "Dr. Andrew Ng",
        "email": "ang@cs.stanford.edu",
        "institution": "Stanford University",
        "department": "Computer Science",
        "title": "Adjunct Professor",
        "homepage_url": "https://www.andrewng.org",
        "research_topics": "Autonomous Agents, Multi-Agent Collaboration, Data-Centric AI",
        "accepting_students": "Yes",
        "status": "Reviewing",
        "match_score": 9.3,
        "papers": [
            {
                "title": "Agentic Design Patterns for LLMs",
                "year": 2024,
                "venue": "DeepLearning.AI Report",
                "abstract": "We analyze four design patterns for LLM agents: reflection, tool use, planning, and multi-agent collaboration. Empirical results show agentic workflows dramatically outperform zero-shot generation across coding and reasoning benchmarks."
            },
            {
                "title": "Data-Centric AI: Shifting the Focus from Code to Data",
                "year": 2023,
                "venue": "IEEE Computer",
                "abstract": "Proposing a systematic methodology for engineering data to improve machine learning accuracy, demonstrating that iterative dataset curation yields greater gains than model architecture tweaks."
            }
        ]
    },
    {
        "name": "Dr. Chelsea Finn",
        "email": "cbfinn@cs.stanford.edu",
        "institution": "Stanford University",
        "department": "Computer Science & Electrical Engineering",
        "title": "Associate Professor",
        "homepage_url": "https://ai.stanford.edu/~cbfinn/",
        "research_topics": "Meta-Learning, Robotic Manipulation, Offline Reinforcement Learning",
        "accepting_students": "Yes",
        "status": "Identified",
        "match_score": 8.7,
        "papers": [
            {
                "title": "Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks",
                "year": 2023,
                "venue": "ICML",
                "abstract": "An algorithm for meta-learning that is compatible with any model trained with gradient descent and applicable to a variety of learning problems, including classification, regression, and policy gradient reinforcement learning."
            }
        ]
    },
    {
        "name": "Dr. Yann LeCun",
        "email": "yann@cs.nyu.edu",
        "institution": "New York University (NYU)",
        "department": "Courant Institute of Mathematical Sciences",
        "title": "Silver Professor of Computer Science",
        "homepage_url": "https://yann.lecun.com",
        "research_topics": "World Models, Joint Embedding Predictive Architecture (JEPA), Self-Supervised Learning",
        "accepting_students": "Grant_Funded",
        "status": "Identified",
        "match_score": 8.9,
        "papers": [
            {
                "title": "A Path Towards Autonomous Machine Intelligence",
                "year": 2023,
                "venue": "OpenReview / arXiv",
                "abstract": "Proposing an architecture and training paradigms for constructing autonomous intelligent agents based on Hierarchical Joint Embedding Predictive Architecture (H-JEPA) without auto-regressive token generation bottlenecks."
            }
        ]
    },
    {
        "name": "Dr. Pieter Abbeel",
        "email": "pabbeel@cs.berkeley.edu",
        "institution": "UC Berkeley",
        "department": "EECS",
        "title": "Professor",
        "homepage_url": "https://people.eecs.berkeley.edu/~pabbeel/",
        "research_topics": "Deep Reinforcement Learning, Robotic Learning, Foundation Models for Robotics",
        "accepting_students": "Yes",
        "status": "Draft_Ready",
        "match_score": 9.1,
        "papers": [
            {
                "title": "End-to-End Robotic Manipulation with Vision-Language-Action Models",
                "year": 2024,
                "venue": "CoRL",
                "abstract": "Investigating how multimodal foundation models pretrained on internet data can be adapted for robotic embodiment and dexterity."
            }
        ]
    }
]

async def seed():
    await init_db()
    async with AsyncSessionLocal() as session:
        # Check if default candidate user exists
        stmt = select(User).where(User.email == "candidate.test@stanford.edu")
        res = await session.execute(stmt)
        user = res.scalar_one_or_none()

        if not user:
            user = User(
                email="candidate.test@stanford.edu",
                hashed_password=hash_password("SecurePassword123!"),
                full_name="Sumit Raj",
                target_field="Computer Science & Artificial Intelligence",
                current_degree="M.S. in Computer Science",
                research_interests="Large Language Models, Multi-Agent Systems, Agentic Workflows",
                cv_summary="NeurIPS workshop author. Strong background in PyTorch, distributed inference, and RLHF fine-tuning."
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print("[PASS] Created seed user: candidate.test@stanford.edu")

        # Check existing professors
        prof_stmt = select(Professor).where(Professor.user_id == user.id)
        existing_profs = (await session.execute(prof_stmt)).scalars().all()
        existing_names = {p.name for p in existing_profs}

        for p_data in SEED_PROFESSORS:
            if p_data["name"] in existing_names:
                continue

            prof = Professor(
                user_id=user.id,
                name=p_data["name"],
                email=p_data["email"],
                institution=p_data["institution"],
                department=p_data["department"],
                title=p_data["title"],
                homepage_url=p_data["homepage_url"],
                research_topics=p_data["research_topics"],
                accepting_students=p_data["accepting_students"],
                status=p_data["status"],
                match_score=p_data["match_score"]
            )
            session.add(prof)
            await session.flush()

            for paper_data in p_data["papers"]:
                paper = Paper(
                    professor_id=prof.id,
                    title=paper_data["title"],
                    year=paper_data["year"],
                    venue=paper_data["venue"],
                    abstract=paper_data["abstract"]
                )
                session.add(paper)

            print(f"[PASS] Seeded professor: {prof.name} ({prof.institution})")

        await session.commit()
        print("[PASS] Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed())

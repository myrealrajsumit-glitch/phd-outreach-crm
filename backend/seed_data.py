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
        stmt = select(User).where(User.email == "er.raj.sumit49@gmail.com")
        res = await session.execute(stmt)
        user = res.scalar_one_or_none()

        cv_summary = """AI/ML-oriented civil engineer and MSc graduate (Project & Infrastructure Management, Brunel University London, Merit) working at the intersection of machine learning, construction project controls, and infrastructure decision-making. Current research applies Python-based data pipelines and supervised learning models (Random Forest, Decision Tree, Linear Regression, KNN, Naive Bayes) to construction schedule, cost, progress, and resource data, generating interpretable, evidence-based risk indicators for project decision support. Combines applied industry experience as Project Engineer at Armour Construction, Tesco, and Kriach Infrastructure with peer-reviewed publication authorship and a national Best Paper Award (NEEV 2017).

Key Research & Academic Portfolio:
- AI-Assisted Project Monitoring & Risk Prediction System for Construction Projects (Armour Construction, Indore): Designed data-driven framework integrating construction schedules, cost records, and site-progress data; trained Random Forest and Decision Tree models to predict schedule delays, cost overruns, and resource conflicts; built Python/Pandas data pipelines for cleaning, validation, and BIM-derived analysis; created interpretable risk visualisations for human-AI decision support.
- MSc Dissertation (Brunel University London): 'BIM for Construction Project Monitoring & Payment Certification' — investigated integration of BIM into real-time monitoring and payment certification workflows.
- Academic Performance: MSc Merit from Brunel University London (Grade A/A+ in Research Methods, Infrastructure Management, Sustainable Project Management, Quality Management & Reliability). B.E. Civil Engineering Honours (80%).
- Publications:
  1. 'Expansive Soil Modification by the Application of Different Waste Materials' (IJTIMES, 2018)
  2. 'E-waste as a Replacement for Aggregate in M-25 Concrete' (IJRDET, 2017)
- Awards: Best Paper Award (National-Level NEEV 2017), Champion SAMEEKSHA Technical Championship, First Place SRUJAN Science & Tech Exhibition.
- Technical Skills: Python (Pandas, NumPy, Scikit-learn, Matplotlib), Power BI, BIM, AutoCAD, Revit, MS Project, STAAD Pro, MATLAB.
- Academic References: Dr. Andrew Fox (Vice Dean Education / Senior Lecturer, Brunel University London) & Dr. Muhammad Shafique (Lecturer, Brunel University London)."""

        target_field = "AI/ML for Construction & Infrastructure Systems | Predictive Risk Analytics & Digital Construction"
        degree = "MSc Project and Infrastructure Management (Merit, Brunel University London, 2023) | B.E. Civil Engineering (Honours, 80%)"
        interests = "AI/ML for Construction & Infrastructure Systems, Predictive Construction Risk Analytics, Cost & Schedule Forecasting Models, AI-Assisted Project Monitoring, BIM + AI / Digital Construction, Data-Driven Project Controls, Human-AI Decision Support, Sustainable & Resilient Infrastructure"

        if not user:
            user = User(
                email="er.raj.sumit49@gmail.com",
                hashed_password=hash_password("SecurePassword123!"),
                full_name="Sumit Raj",
                target_field=target_field,
                current_degree=degree,
                research_interests=interests,
                cv_summary=cv_summary
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print("[PASS] Created seed user: er.raj.sumit49@gmail.com (Sumit Raj)")
        else:
            user.full_name = "Sumit Raj"
            user.target_field = target_field
            user.current_degree = degree
            user.research_interests = interests
            user.cv_summary = cv_summary
            await session.commit()
            print("[PASS] Updated existing seed user profile to Brunel MSc with Merit")

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

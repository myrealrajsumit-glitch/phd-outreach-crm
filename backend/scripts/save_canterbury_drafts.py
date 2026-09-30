import asyncio
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.professor import Professor
from app.models.email import EmailDraft

EMAILS_DATA = [
    {
        "name": "Dr. Daniel van der Walt",
        "email": "daniel.vanderwalt@canterbury.ac.nz",
        "institution": "University of Canterbury",
        "department": "Civil and Natural Resources Engineering",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML Research in Construction & Infrastructure",
        "body": """Dear Dr van der Walt,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire whether you may be open to considering me for PhD supervision in the area of AI and machine learning for construction and infrastructure systems.

My interest in AI/ML has developed progressively through my academic and professional journey. My MSc provided me with a foundation in project and infrastructure management and digital construction, including a dissertation on BIM for Construction Project Monitoring and Payment Certification. Through my professional work and subsequent research development, I have increasingly built practical capability in Python, data analysis and supervised machine-learning methods for construction problems.

My current research work applies construction schedules, cost records, site-progress information and historical project-performance data to predictive analysis. I have explored Random Forest, Decision Tree and Linear Regression approaches for risk identification, cost and schedule trend analysis, and evidence-based project decision support.

I believe there is an important research opportunity in developing AI methods that are not simply technically accurate, but are genuinely useful for construction and infrastructure decision-making. In particular, I am interested in addressing the gap between the growing availability of construction data and the limited practical use of robust, interpretable AI models for monitoring, prediction and risk management.

I believe my combination of civil engineering, construction/project-management experience, BIM exposure and developing AI/ML capability could allow me to contribute to this area while also developing the methodological depth required for doctoral research.

Your work involving machine-learning applications in infrastructure and construction monitoring is particularly relevant to this direction. I would therefore like to explore a PhD focused broadly on:

AI/ML-based predictive monitoring, risk detection and interpretable decision support for construction and infrastructure projects.

BIM would be a supporting source of structured project information, while my primary research focus would be AI/ML, predictive modelling, validation, risk analytics and decision support.

I would be very grateful to know whether this research direction could fit your current supervision interests. I am open to both funded and self-funded PhD routes and would be happy to consider either pathway.

I have not attached documents at this initial stage. If you believe my background may be relevant, I would greatly appreciate the opportunity to send you my CV, academic records and a detailed research concept for your consideration.

Thank you very much for your time. I would be grateful for the opportunity to discuss this with you.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Associate Professor Brian Guo",
        "email": "brian.guo@canterbury.ac.nz",
        "institution": "University of Canterbury",
        "department": "Civil and Natural Resources Engineering",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML & Digital Construction Research",
        "body": """Dear Associate Professor Guo,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire whether you may be open to supervising a PhD focused primarily on AI/ML applications in construction management and digital construction.

My research interest in AI/ML has developed progressively. During my MSc, I built a strong foundation in project and infrastructure management and BIM through my dissertation on BIM for Construction Project Monitoring and Payment Certification. During my professional experience and following my MSc, I have further developed my skills in Python, data analysis and machine-learning methods and have applied them to construction project-performance problems.

My current research portfolio involves Python/Pandas-based processing of construction schedules, cost records, site-progress information and historical project-performance data. I have explored Random Forest, Decision Tree and Linear Regression methods for project-risk identification, cost and schedule trend analysis and predictive decision support.

I see a significant research opportunity in connecting the large volume of digital information now generated by construction projects with AI methods capable of producing reliable, interpretable and actionable decision support. In particular, I am interested in the research gap between digital construction/BIM data availability and the development and validation of AI models that can convert that information into useful predictions for project managers.

I believe my background gives me a useful combination of civil engineering knowledge, construction/project-management experience, BIM understanding and hands-on development of AI/ML skills. I would like to strengthen this foundation through doctoral research and contribute to the development of more effective AI applications for construction.

Your work in the construction-management and digital-construction space is particularly relevant to this ambition. I would therefore like to explore a PhD direction around:

AI-driven predictive and intelligent decision-support systems for construction project monitoring and management.

BIM would be an important digital information layer within the research, but my primary research interest is AI/ML—predictive modelling, intelligent information processing, model evaluation, risk identification and decision support.

I would be grateful to know whether this direction could align with your current supervision interests. I am open to both funded and self-funded PhD study and would be willing to consider either route.

I have deliberately not attached documents at this initial stage. If you feel my background may be relevant, I would greatly appreciate the opportunity to send you my CV, academic records and a detailed research concept for your consideration.

Thank you very much for considering my enquiry. I would be grateful for the opportunity to hear your thoughts.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Associate Professor Eric Scheepbouwer",
        "email": "eric.scheepbouwer@canterbury.ac.nz",
        "institution": "University of Canterbury",
        "department": "Civil and Natural Resources Engineering",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML for Construction Risk & Decision Support",
        "body": """Dear Associate Professor Scheepbouwer,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire whether you may be open to considering me for PhD supervision focused on AI/ML-based predictive risk and decision support for construction and infrastructure management.

My AI/ML interest has developed progressively through my academic and professional journey. My MSc established my foundation in project and infrastructure management and BIM, with my dissertation focused on BIM for Construction Project Monitoring and Payment Certification. During my professional experience and after completing my MSc, I have continued to develop my capabilities in Python, data analysis, predictive modelling and machine learning.

My current research work uses construction schedules, cost records, site-progress information and historical project-performance data. I have explored Random Forest and Decision Tree models for risk identification and Linear Regression for cost and schedule trend analysis.

I believe an important research opportunity exists in developing AI systems that can move beyond prediction alone and provide interpretable, evidence-based decision support for construction and infrastructure managers. The research challenge is not simply to apply another machine-learning algorithm, but to determine how AI can be validated, interpreted and integrated into real project decision processes.

This is the research contribution I would like to develop during a PhD: combining my civil engineering and construction-management background with increasingly advanced AI/ML methods to address practical and scientifically meaningful problems in construction risk and project performance.

Given your research environment in construction management, risk, cost and infrastructure decision-making, I would like to explore a PhD direction around:

Machine-learning-based predictive risk and performance modelling for construction and infrastructure decision-making.

BIM would support the digital information environment, but my primary doctoral interest would remain AI/ML, predictive modelling, risk analytics, model validation and decision support.

I would be very grateful to know whether this direction could fit your current supervision interests. I am open to both funded and self-funded PhD routes and would be happy to consider either option.

I have not attached documents at this initial stage. If you believe my background may be relevant, I would be very grateful for the opportunity to send you my CV, academic records and a detailed research concept for your consideration.

Thank you very much for your time and consideration. I would be grateful for the opportunity to discuss this further.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    }
]

async def save_drafts():
    async with AsyncSessionLocal() as session:
        # Find user
        u_res = await session.execute(select(User))
        user = u_res.scalars().first()
        if not user:
            print("No user found in database.")
            return

        print(f"Saving drafts for User: {user.id} ({user.email})...")

        for item in EMAILS_DATA:
            # Check or create professor
            clean_email = item["email"].strip().lower()
            p_stmt = select(Professor).where(
                func.lower(Professor.email) == clean_email,
                Professor.user_id == user.id
            )
            p_res = await session.execute(p_stmt)
            prof = p_res.scalar_one_or_none()

            if not prof:
                prof = Professor(
                    user_id=user.id,
                    name=item["name"],
                    email=clean_email,
                    institution=item["institution"],
                    department=item["department"],
                    status="Draft_Ready"
                )
                session.add(prof)
                await session.commit()
                await session.refresh(prof)
                print(f"Created Professor: {prof.name} ({prof.email})")
            else:
                prof.status = "Draft_Ready"
                await session.commit()
                print(f"Existing Professor: {prof.name} ({prof.email})")

            # Create Email Draft
            draft = EmailDraft(
                professor_id=prof.id,
                subject=item["subject"],
                body=item["body"],
                status="Draft"
            )
            session.add(draft)
            await session.commit()
            await session.refresh(draft)
            print(f"Saved Draft #{draft.id} for {prof.name}")

        print("All 3 drafts successfully saved to PostgreSQL database!")

if __name__ == "__main__":
    asyncio.run(save_drafts())

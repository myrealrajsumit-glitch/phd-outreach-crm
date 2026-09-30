import asyncio
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.professor import Professor
from app.models.email import EmailDraft
from sqlalchemy import select

CANTERBURY_EMAILS = [
    {
        "name": "Dr Ke Jiang",
        "email": "ke.jiang@canterbury.ac.nz",
        "department": "Civil and Natural Resources Engineering",
        "research_interests": "Structural engineering, numerical modelling, machine-learning-based design, resilient steel/aluminium structures",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML for Resilient Structural Engineering",
        "body": """Dear Dr Jiang,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire whether you may be open to considering me for PhD supervision in AI/ML applications to structural engineering and infrastructure resilience.

My primary research interest is AI/ML, developed progressively through my academic and professional experience. My MSc dissertation focused on BIM for Construction Project Monitoring and Payment Certification, while my professional and subsequent research development has involved Python, data analysis and machine-learning methods applied to construction project-performance and risk problems.

I was particularly interested in your research combining structural engineering, numerical modelling and machine-learning-based design methods, including work on resilient steel/aluminium structures and structures exposed to hazards.

I see a strong research opportunity in developing AI/ML models that can complement mechanics-based methods for structural assessment, prediction and resilient design. My civil-engineering background could provide the engineering application context, while I would like the doctoral research to make a stronger methodological contribution in AI/ML, model validation and interpretable prediction.

A possible direction I would like to explore is machine-learning-assisted structural risk assessment and resilient design for advanced infrastructure systems, with the precise research question developed around your current work.

I would be grateful to know whether this direction could fit your current supervision interests. I am open to both funded and self-funded PhD routes.

I have not attached documents at this initial stage. If you feel my background may be relevant, I would greatly appreciate the opportunity to send you my CV, academic records and a detailed research concept for your consideration.

Thank you very much for your time and consideration.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Dr James Williams",
        "email": "james.williams@canterbury.ac.nz",
        "department": "Civil and Natural Resources Engineering",
        "research_interests": "Data science and machine learning for infrastructure, asset maintenance, statutory inspection",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML & Data Science for Infrastructure",
        "body": """Dear Dr Williams,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am contacting you because my primary doctoral interest is AI/ML and data science applied to construction and infrastructure, and your work appears particularly relevant to this direction.

My AI/ML development has progressed through my professional work and research development. I currently work with Python, Pandas, data preparation and supervised-learning methods, applying Random Forest, Decision Tree and Linear Regression to construction schedules, cost records, site-progress information and historical project-performance data.

I was particularly interested in your work applying data science and machine learning to infrastructure, asset maintenance and statutory inspection, as well as your involvement in industry-linked data-science projects at UC.

This creates a strong methodological connection with the research direction I want to pursue: developing AI systems that can convert engineering and infrastructure data into reliable predictions, risk indicators and decision-support tools.

A possible PhD direction is AI/ML-based predictive analytics for construction and infrastructure asset/project performance, potentially addressing model validation, data quality, explainability and practical deployment in engineering environments.

I believe my construction and infrastructure background could provide a useful application domain while your data-science and machine-learning expertise could help me develop the methodological depth required for doctoral research.

I would be grateful to know whether you might be open to discussing potential supervision. I am open to both funded and self-funded PhD routes.

I have deliberately not attached documents at this initial stage. If you feel there may be a research fit, I would appreciate the opportunity to send my CV, academic records and a detailed research concept for your consideration.

Thank you very much for your time.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Professor Brendon Bradley",
        "email": "brendon.bradley@canterbury.ac.nz",
        "department": "Civil and Natural Resources Engineering",
        "research_interests": "Strong ground-motion prediction, seismic performance, loss estimation, risk-informed decision-making for resilient infrastructure",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML for Infrastructure Risk & Resilience",
        "body": """Dear Professor Bradley,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire about a possible PhD focused on AI/ML, infrastructure risk and resilient engineering systems.

My primary research interest is AI/ML, supported by a civil-engineering and project/infrastructure-management background. My MSc dissertation examined BIM for Construction Project Monitoring and Payment Certification, and my subsequent research development has involved Python-based data analysis and machine-learning methods for construction risk and project-performance prediction.

I was particularly interested in your research on strong ground-motion prediction, seismic performance, loss estimation and risk-informed decision-making for resilient infrastructure. These areas present an important opportunity for advanced predictive modelling.

I would like to investigate how AI/ML could complement established engineering and risk models by learning from large and heterogeneous datasets while retaining appropriate engineering interpretation, validation and uncertainty assessment.

A possible research direction is AI/ML-enhanced risk prediction and decision support for resilient infrastructure systems, with construction and infrastructure management providing the broader application context.

I would be grateful to know whether such a direction could align with your current research and supervision interests. I am open to both funded and self-funded PhD routes.

I have not attached documents at this initial stage. If you believe my background could be relevant, I would appreciate the opportunity to send my CV, academic records and detailed research concept.

Thank you for your time and consideration.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Professor Larry Bellamy",
        "email": "larry.bellamy@canterbury.ac.nz",
        "department": "Civil and Natural Resources Engineering",
        "research_interests": "Low-carbon and climate-resilient buildings, digital design and construction methods",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML & Digital Infrastructure Performance",
        "body": """Dear Professor Bellamy,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire whether you may be open to considering a PhD exploring AI/ML for building and infrastructure performance.

My primary interest is AI/ML. My MSc provided a foundation in project and infrastructure management and BIM, including a dissertation on BIM for Construction Project Monitoring and Payment Certification. Since then, I have developed Python, data-analysis and machine-learning skills and applied them to construction project monitoring, risk identification and performance prediction.

Your research in low-carbon and climate-resilient buildings and infrastructure, verification methods, and digital methods for building design and construction is particularly relevant to the application domain I would like to study.

I see a research opportunity in using AI/ML to integrate building and infrastructure performance data with digital construction information to support prediction, verification, risk assessment and decision-making for resilient and sustainable assets.

A possible PhD direction is AI/ML-based predictive performance and decision-support systems for sustainable and resilient buildings and infrastructure.

I would be grateful to know whether this direction could fit within your current research and supervision interests. I am open to both funded and self-funded PhD routes.

I have deliberately not attached documents at this stage. If you feel there may be a research fit, I would greatly appreciate the opportunity to send my CV, academic records and detailed research concept.

Thank you very much for your time.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Dr Tom Logan",
        "email": "tom.logan@canterbury.ac.nz",
        "department": "Civil and Natural Resources Engineering",
        "research_interests": "Systemic risk, cascading risks, resilience planning, climate adaptation uncertainty",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML for Infrastructure Risk & Resilience",
        "body": """Dear Dr Logan,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire about potential PhD supervision in AI/ML, infrastructure risk and resilient decision-making.

My primary research interest is AI/ML, developed through professional and research work alongside my civil-engineering and infrastructure-management background. I have developed Python/Pandas workflows using construction schedules, cost records, site-progress data and historical project-performance information, and explored machine-learning methods for project-risk identification and prediction.

I was particularly interested in your current work on systemic risk, cascading risks, resilience planning and uncertainty in climate adaptation. The systemic nature of infrastructure risk creates an interesting opportunity for AI/ML methods that can learn relationships across interconnected infrastructure systems.

I would like to investigate whether AI/ML can contribute to infrastructure risk analysis by combining heterogeneous data sources, identifying emerging risk patterns and supporting interpretable decision-making under uncertainty.

A possible PhD direction is AI/ML-based predictive and systemic risk analysis for resilient infrastructure networks, with construction/infrastructure management as the application domain.

I would be grateful to know whether this direction might fit your current research. I am open to both funded and self-funded PhD routes.

I have not attached documents at this initial stage. If you see potential alignment, I would appreciate the opportunity to send my CV, academic records and detailed research concept.

Thank you very much for your consideration.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Dr Rebecca Peer",
        "email": "rebecca.peer@canterbury.ac.nz",
        "department": "Civil Systems Engineering / Sustainable Energy Research",
        "research_interests": "Data-driven modelling for resilient infrastructure systems, energy systems, uncertainty",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML & Resilient Infrastructure Systems",
        "body": """Dear Dr Peer,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire whether you may be open to discussing PhD supervision involving AI/ML, data-driven modelling and resilient infrastructure systems.

My primary research interest is AI/ML. My civil-engineering background and MSc in project/infrastructure management provide the application context, while my subsequent research development has focused on Python, data analysis and supervised machine learning for construction project risk and performance.

I am particularly interested in UC's Civil Systems Engineering and Sustainable Energy Research environments, where modelling, optimisation, resilience, uncertainty and infrastructure systems are studied together. Your work within the Sustainable Energy Research Group is especially relevant to my interest in data-driven approaches for complex infrastructure systems.

I would like to explore whether AI/ML can improve prediction and decision-making in complex infrastructure systems, particularly where multiple uncertainties, interacting components and resilience considerations must be addressed.

A possible PhD direction is AI/ML-based predictive modelling and decision support for resilient infrastructure systems, with the precise application developed around your current research.

I would be grateful to know whether this could fit your supervision interests. I am open to both funded and self-funded PhD routes.

I have not attached documents at this stage. If you see potential research alignment, I would appreciate the opportunity to send my CV, academic records and detailed research concept.

Thank you for your time and consideration.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Associate Professor Jannik Haas",
        "email": "jannik.haas@canterbury.ac.nz",
        "department": "Civil Systems Engineering / Sustainable Energy Research Group",
        "research_interests": "Energy systems modelling, optimisation, resilience and uncertainty",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML for Resilient Infrastructure & Energy Systems",
        "body": """Dear Associate Professor Haas,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am contacting you to explore whether my background could fit a PhD involving AI/ML, predictive modelling and resilient infrastructure systems.

My primary research interest is AI/ML. My MSc foundation is in project and infrastructure management, including BIM-based project monitoring, while my subsequent research development has focused on Python, data analysis and machine-learning approaches to construction risk and project-performance prediction.

I was particularly interested in your research on energy systems modelling, optimisation, resilience and uncertainty, and the Sustainable Energy Research Group's work on modelling resilient infrastructure systems.

I see an opportunity to investigate AI/ML methods for predictive modelling and decision support in infrastructure systems where demand, climate, technology and operational conditions are uncertain. My construction/infrastructure background could provide an engineering application perspective while the research develops stronger AI/ML methodology.

A possible direction is AI/ML-enhanced predictive modelling and decision support for resilient infrastructure systems under uncertainty.

I understand from your current UC profile that the group is interested in PhD candidates with scholarship funding or candidates competitive for UC Doctoral Scholarships, and that 2027 research opportunities are being developed. I would therefore be grateful to discuss both possibilities.

I am open to both funded and self-funded PhD routes.

I have deliberately not attached documents at this initial stage. If you believe my background may be relevant, I would greatly appreciate the opportunity to send my CV, academic records and a detailed research concept.

Thank you very much for your time.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Dr Wai Wong",
        "email": "wai.wong@canterbury.ac.nz",
        "department": "Civil and Natural Resources Engineering",
        "research_interests": "Connected and automated vehicles, real-time data, adaptive traffic signal control, smart transport systems",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML & Smart Infrastructure Systems",
        "body": """Dear Dr Wong,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire whether you may be open to considering a PhD focused on AI/ML and intelligent infrastructure systems.

My primary research interest is AI/ML, supported by a civil-engineering and project/infrastructure-management background. My subsequent research development has involved Python, data analysis and machine-learning methods applied to construction schedules, cost, progress and project risk.

I was particularly interested in your research on connected and automated vehicles, real-time data, adaptive traffic signal control and smart transport systems. Your current work addresses the challenge of making infrastructure decisions from incomplete and continuously changing information, which is closely related to the type of AI decision-support problem I would like to investigate.

I would like to explore how machine-learning methods can combine heterogeneous infrastructure data to predict system states, identify emerging risks and support adaptive decisions in real-world infrastructure environments.

A possible direction is AI/ML-based predictive and adaptive decision support for smart construction and infrastructure systems, with transport infrastructure as one possible application domain.

I would be grateful to know whether this direction could fit your current research interests. I am open to both funded and self-funded PhD routes.

I have not attached documents at this initial stage. If you feel there may be a research fit, I would greatly appreciate the opportunity to send my CV, academic records and detailed research concept.

Thank you very much for your consideration.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Professor Daniel Nilsson",
        "email": "daniel.nilsson@canterbury.ac.nz",
        "department": "Civil and Natural Resources Engineering",
        "research_interests": "Evacuation systems, human interaction with infrastructure, safety decision-making, disaster resilience",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML, Modelling & Infrastructure Safety",
        "body": """Dear Professor Nilsson,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire about potential PhD supervision involving AI/ML, modelling and intelligent decision support for infrastructure safety and resilience.

My primary research interest is AI/ML. My background combines civil engineering, project/infrastructure management and construction project monitoring, followed by continued development of Python, data analysis and machine-learning skills. My current research uses construction and project-performance data to investigate risk and predictive decision support.

I was particularly interested in your work on evacuation systems, human interaction with infrastructure, VR-based experiments and safety decision-making. UC also currently advertises a funded PhD project on next-generation tsunami evacuation modelling involving modelling, programming and infrastructure/disaster mitigation, with you as primary supervisor.

This environment interests me because it demonstrates how computational modelling and real-world infrastructure problems can be combined to improve safety decisions. I would like to explore whether AI/ML could strengthen such modelling through predictive analysis, pattern recognition or intelligent decision support.

A possible direction is AI/ML-enhanced predictive modelling and decision support for infrastructure safety, evacuation and disaster resilience.

I would be grateful to know whether you may be open to discussing potential supervision. I am open to both funded and self-funded PhD routes.

I have not attached documents at this initial stage. If you believe my background may be relevant, I would appreciate the opportunity to send my CV, academic records and detailed research concept.

Thank you very much for your time.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Associate Professor Richard Clare",
        "email": "richard.clare@canterbury.ac.nz",
        "department": "Electrical and Computer Engineering",
        "research_interests": "Image processing, computational imaging, machine learning, infrastructure monitoring",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML, Computer Vision & Infrastructure Monitoring",
        "body": """Dear Associate Professor Clare,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire whether you may be open to considering me for PhD supervision involving AI/ML, computational imaging and infrastructure monitoring.

My primary research interest is AI/ML. My civil-engineering background provides the application domain, while my MSc dissertation gave me experience with BIM-based project monitoring and my subsequent research development has involved Python, data analysis and machine-learning approaches for construction risk and project-performance prediction.

I was particularly interested in your work in image processing, computational imaging and machine learning, as well as your supervision of postgraduate research involving machine learning.

I see a potential research opportunity in applying computer-vision and machine-learning techniques to engineering environments, where visual or imaging data could complement conventional project and infrastructure information for automated monitoring, condition assessment and risk detection.

A possible direction is AI/ML and computer-vision-based monitoring and predictive assessment of construction and infrastructure assets.

I would be interested in exploring whether techniques from computational imaging and machine learning could be adapted to engineering data while maintaining robust validation and practical interpretability.

I would be grateful to know whether this research direction could fit your current supervision interests. I am open to both funded and self-funded PhD routes.

I have deliberately not attached documents at this initial stage. If you feel there may be a research fit, I would greatly appreciate the opportunity to send you my CV, academic records and a detailed research concept for your consideration.

Thank you very much for your time and consideration.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Professor David Dempsey",
        "email": "david.dempsey@canterbury.ac.nz",
        "department": "Civil and Natural Resources Engineering",
        "research_interests": "Machine-learning applications in engineering prediction and risk, geological/infrastructure modelling",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML for Infrastructure Risk & Prediction",
        "body": """Dear Professor Dempsey,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire whether you may be open to considering me for PhD supervision in the area of AI and machine learning for infrastructure and engineering decision-making.

My interest in AI/ML has developed progressively through my academic and professional journey. My MSc provided me with a foundation in project and infrastructure management and digital construction, with my dissertation focusing on BIM for Construction Project Monitoring and Payment Certification. During my professional experience and following my MSc, I have continued to develop my skills in Python, data analysis and supervised machine-learning methods and have applied them to construction project-performance and risk problems.

My current research work involves construction schedules, cost records, site-progress information and historical project-performance data. I have explored Random Forest, Decision Tree and Linear Regression approaches for risk identification, cost and schedule trend analysis and predictive decision support.

I am particularly interested in the research challenge of developing AI systems that can learn from engineering data and provide reliable, interpretable predictions that can support real-world infrastructure decisions. I believe there remains considerable scope to improve the transferability, validation and practical use of machine-learning models in engineering systems, particularly where decisions involve uncertainty, limited data and potentially significant infrastructure consequences.

I believe my combination of civil engineering, construction/project-management experience, BIM exposure and developing AI/ML capability could allow me to contribute to this area while also developing the methodological depth required for doctoral research.

Your work involving machine-learning applications in engineering prediction and risk is particularly relevant to this direction. I would therefore like to explore a PhD focused broadly on:

AI/ML-based predictive modelling and risk-informed decision support for infrastructure and engineering systems.

My construction and infrastructure background would provide the application domain, while my primary research interest would be the development, validation and interpretation of AI/ML models.

I am also interested in how digital construction and BIM-derived information could provide structured data for such models, but I see AI/ML as the central research contribution.

I would be very grateful to know whether this direction could potentially align with your current research and supervision interests. I am open to both funded and self-funded PhD routes and would be happy to consider either pathway.

I have deliberately not attached documents at this initial stage. If you feel that my background may be relevant, I would greatly appreciate the opportunity to send you my CV, academic records and a more detailed research concept for your consideration.

Thank you very much for your time. I would be grateful for the opportunity to discuss this with you.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Dr Alberto Ardid",
        "email": "alberto.ardid@canterbury.ac.nz",
        "department": "Civil and Natural Resources Engineering",
        "research_interests": "Artificial intelligence, machine learning and predictive modelling applied to engineering and geophysical problems under uncertainty",
        "subject": "Prospective PhD – Funded or Self-Funded | AI/ML, Predictive Modelling & Engineering",
        "body": """Dear Dr Ardid,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire whether you may be open to considering me for PhD supervision in artificial intelligence, machine learning and predictive modelling applied to engineering and infrastructure problems.

My interest in AI/ML has developed progressively through my academic and professional experience. My MSc was in Project and Infrastructure Management, with my dissertation focusing on BIM for Construction Project Monitoring and Payment Certification. During my professional work and after completing my MSc, I have continued developing my skills in Python, data analysis and machine learning and have increasingly applied these methods to construction and infrastructure-related problems.

My current research work uses construction schedules, cost records, site-progress information and historical project-performance data. I have worked with Random Forest, Decision Tree and Linear Regression approaches for risk identification, cost and schedule trend analysis and predictive decision support.

What particularly interests me about your research is the methodological challenge of using real-world engineering data to develop predictive AI systems under uncertainty. I see a significant research opportunity in improving the reliability, interpretability, transferability and practical deployment of AI/ML models for engineering decision-making, particularly where data are heterogeneous, incomplete or generated continuously.

I would therefore like to explore a PhD direction broadly focused on:

AI/ML-based predictive modelling and uncertainty-aware decision support for construction and infrastructure systems.

Construction and infrastructure would provide the application domain, while the central research contribution would be the development and rigorous evaluation of AI/ML methodologies.

I believe my existing experience gives me a useful starting point: civil engineering and infrastructure knowledge, project-management experience, exposure to BIM and construction data, and hands-on development of Python and machine-learning skills. I would now like to develop this foundation into deeper methodological research through doctoral study.

I would be very grateful to know whether this direction could fit within your current research and supervision interests. I am open to both funded and self-funded PhD routes and would be happy to consider either pathway.

I have deliberately not attached documents at this initial stage. If you feel my background may be relevant, I would greatly appreciate the opportunity to send you my CV, academic records and a detailed research concept for your consideration.

Thank you very much for your time and consideration. I would be grateful for the opportunity to discuss this further.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    },
    {
        "name": "Professor Richard Green",
        "email": "richard.green@canterbury.ac.nz",
        "department": "Computer Science and Software Engineering",
        "research_interests": "Computer vision, AI, real-time 3D reconstruction and tracking",
        "subject": "Prospective PhD – Funded or Self-Funded | AI, Computer Vision & Infrastructure",
        "body": """Dear Professor Green,

I hope you are well.

My name is Sumit Raj, a Civil Engineer with an MSc in Project and Infrastructure Management from Brunel University London, awarded with Merit. I am writing to enquire whether you may be open to considering me for PhD supervision in artificial intelligence, machine learning and computer-vision-based applications for construction and infrastructure.

My primary research interest is AI/ML. My academic and professional background provides the engineering application domain through civil engineering, construction and infrastructure management. My MSc dissertation focused on BIM for Construction Project Monitoring and Payment Certification, while during my professional experience and following my MSc I have continued developing my skills in Python, data analysis and machine learning.

My current research work focuses on using construction schedules, cost records, site-progress information and historical project-performance data to develop predictive risk and project-monitoring approaches. I have worked with Random Forest, Decision Tree and Linear Regression methods and have an increasing interest in extending these approaches toward richer forms of automated data interpretation.

I was particularly interested in your research in computer vision, AI, real-time 3D reconstruction and tracking. I see a potentially important research opportunity in applying advanced computer vision and AI methods to construction and infrastructure environments, where visual data from cameras, drones or other sensing systems could potentially be combined with project and engineering data to support automated progress monitoring, condition assessment, risk identification and decision-making.

I would therefore like to explore a PhD direction broadly focused on:

AI and computer-vision-based intelligent monitoring and decision support for construction and infrastructure systems.

My interest is not limited to applying an existing computer-vision model to construction. I would like to investigate how AI methods, visual information and engineering/project data could be integrated and rigorously evaluated to create reliable and interpretable systems for real-world infrastructure applications.

BIM would be a supporting digital-information layer where appropriate, but my primary research interest remains AI/ML, computer vision, predictive modelling and intelligent decision support.

I would be very grateful to know whether you consider this direction potentially compatible with your current research and supervision interests. I am open to both funded and self-funded PhD routes and would be happy to consider either pathway.

I have deliberately not attached documents at this initial stage. If you feel that my background may be relevant, I would greatly appreciate the opportunity to send you my CV, academic records and a detailed research concept for your consideration.

Thank you very much for your time. I would be grateful for the opportunity to discuss this with you.

Kind regards,
Sumit Raj
MSc Project and Infrastructure Management — Merit
B.E. Civil Engineering
Email: er.raj.sumit49@gmail.com
Phone: +91 92382 76845"""
    }
]

async def save_canterbury_batch_2():
    async with AsyncSessionLocal() as session:
        user_stmt = select(User).where(User.id == 1)
        user_res = await session.execute(user_stmt)
        user = user_res.scalar_one_or_none()
        if not user:
            print("User 1 not found!")
            return

        added_drafts = 0
        added_profs = 0

        for item in CANTERBURY_EMAILS:
            # Check or create professor
            prof_stmt = select(Professor).where(Professor.email == item["email"], Professor.user_id == user.id)
            prof_res = await session.execute(prof_stmt)
            prof = prof_res.scalar_one_or_none()

            if not prof:
                prof = Professor(
                    user_id=user.id,
                    name=item["name"],
                    email=item["email"],
                    institution="University of Canterbury",
                    department=item.get("department", "Civil Engineering"),
                    research_topics=item.get("research_interests", "AI/ML & Infrastructure"),
                    country="New Zealand",
                    status="Draft_Ready"
                )
                session.add(prof)
                await session.flush()
                await session.refresh(prof)
                added_profs += 1
                print(f"Created Professor: {prof.name} (ID: {prof.id})")
            else:
                prof.status = "Draft_Ready"
                print(f"Found Professor: {prof.name} (ID: {prof.id})")

            # Check if draft already exists
            draft_stmt = select(EmailDraft).where(EmailDraft.professor_id == prof.id, EmailDraft.subject == item["subject"])
            draft_res = await session.execute(draft_stmt)
            draft = draft_res.scalar_one_or_none()

            if not draft:
                draft = EmailDraft(
                    professor_id=prof.id,
                    subject=item["subject"],
                    body=item["body"],
                    status="Draft"
                )
                session.add(draft)
                added_drafts += 1
                print(f"  -> Added Draft for {prof.name}")
            else:
                draft.body = item["body"]
                draft.status = "Draft"
                print(f"  -> Updated Draft for {prof.name}")

        await session.commit()
        print(f"\nSuccessfully saved {added_profs} new professors and {added_drafts} new email drafts for University of Canterbury!")

if __name__ == "__main__":
    asyncio.run(save_canterbury_batch_2())

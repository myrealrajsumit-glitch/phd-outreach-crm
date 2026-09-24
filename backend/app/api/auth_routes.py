from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.models.user import User
from app.config import settings
from app.schemas.user import UserCreate, UserLogin, UserUpdate, UserResponse, Token, SMTPSettingsUpdate

router = APIRouter(prefix="/auth", tags=["Authentication"])
async def get_current_user(
    db: AsyncSession = Depends(get_db)
) -> User:
    result = await db.execute(select(User).order_by(User.id.asc()).limit(1))
    user = result.scalar_one_or_none()
    if not user:
        user = User(
            email="er.raj.sumit49@gmail.com",
            hashed_password=hash_password("SecurePassword123!"),
            full_name="Sumit Raj",
            target_field="AI/ML for Construction & Infrastructure Systems | Predictive Risk Analytics & Digital Construction",
            current_degree="MSc Project and Infrastructure Management (Merit, Brunel University London, 2023) | B.E. Civil Engineering (Honours, 80%)",
            research_interests="AI/ML for Construction & Infrastructure Systems, Predictive Construction Risk Analytics, Cost & Schedule Forecasting Models, AI-Assisted Project Monitoring, BIM + AI / Digital Construction, Data-Driven Project Controls, Human-AI Decision Support, Sustainable & Resilient Infrastructure",
            cv_summary="""AI/ML-oriented civil engineer and MSc graduate (Project & Infrastructure Management, Brunel University London, Merit) working at the intersection of machine learning, construction project controls, and infrastructure decision-making. Current research applies Python-based data pipelines and supervised learning models (Random Forest, Decision Tree, Linear Regression, KNN, Naive Bayes) to construction schedule, cost, progress, and resource data, generating interpretable, evidence-based risk indicators for project decision support. Combines applied industry experience as Project Engineer at Armour Construction, Tesco, and Kriach Infrastructure with peer-reviewed publication authorship and a national Best Paper Award (NEEV 2017).

Key Research & Academic Portfolio:
- AI-Assisted Project Monitoring & Risk Prediction System for Construction Projects (Armour Construction, Indore): Designed data-driven framework integrating construction schedules, cost records, and site-progress data; trained Random Forest and Decision Tree models to predict schedule delays, cost overruns, and resource conflicts; built Python/Pandas data pipelines for cleaning, validation, and BIM-derived analysis; created interpretable risk visualisations for human-AI decision support.
- MSc Dissertation (Brunel University London): 'BIM for Construction Project Monitoring & Payment Certification' — investigated integration of BIM into real-time monitoring and payment certification workflows.
- Academic Performance: MSc Merit from Brunel University London (Grade A/A+ in Research Methods, Infrastructure Management, Sustainable Project Management, Quality Management & Reliability). B.E. Civil Engineering Honours (80%).
- Publications:
  1. 'Expansive Soil Modification by the Application of Different Waste Materials' (IJTIMES, 2018)
  2. 'E-waste as a Replacement for Aggregate in M-25 Concrete' (IJRDET, 2017)
- Awards: Best Paper Award (National-Level NEEV 2017), Champion SAMEEKSHA Technical Championship, First Place SRUJAN Science & Tech Exhibition.
- Technical Skills: Python (Pandas, NumPy, Scikit-learn, Matplotlib), Power BI, BIM, AutoCAD, Revit, MS Project, STAAD Pro, MATLAB.
- Academic References: Dr. Andrew Fox (Vice Dean Education / Senior Lecturer, Brunel University London) & Dr. Muhammad Shafique (Lecturer, Brunel University London).""",
            smtp_host=settings.SMTP_HOST,
            smtp_port=settings.SMTP_PORT,
            smtp_user=settings.SMTP_USER or "er.raj.sumit49@gmail.com",
            smtp_password=settings.SMTP_PASSWORD,
            smtp_from_name=settings.SMTP_FROM_NAME or "Sumit Raj",
            smtp_use_tls=settings.SMTP_USE_TLS
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    elif not user.smtp_password and settings.SMTP_PASSWORD:
        user.smtp_host = settings.SMTP_HOST
        user.smtp_port = settings.SMTP_PORT
        user.smtp_user = settings.SMTP_USER or user.email
        user.smtp_password = settings.SMTP_PASSWORD
        user.smtp_from_name = settings.SMTP_FROM_NAME or user.full_name
        user.smtp_use_tls = settings.SMTP_USE_TLS
        await db.commit()
        await db.refresh(user)
    return user

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        target_field=user_data.target_field,
        current_degree=user_data.current_degree,
        research_interests=user_data.research_interests,
        cv_summary=user_data.cv_summary,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id), "email": new_user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            **new_user.__dict__,
            "smtp_configured": bool(new_user.smtp_host and new_user.smtp_user)
        }
    }

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.")

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            **user.__dict__,
            "smtp_configured": bool(user.smtp_host and user.smtp_user)
        }
    }

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.")

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            **user.__dict__,
            "smtp_configured": bool(user.smtp_host and user.smtp_user and user.smtp_password)
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return {
        **current_user.__dict__,
        "smtp_configured": bool(current_user.smtp_host and current_user.smtp_user and current_user.smtp_password)
    }

@router.put("/me", response_model=UserResponse)
async def update_profile(
    updates: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    for field, val in updates.model_dump(exclude_unset=True).items():
        setattr(current_user, field, val)
    await db.commit()
    await db.refresh(current_user)
    return {
        **current_user.__dict__,
        "smtp_configured": bool(current_user.smtp_host and current_user.smtp_user and current_user.smtp_password)
    }

@router.put("/me/smtp")
async def update_smtp_settings(
    settings_data: SMTPSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    current_user.smtp_host = settings_data.smtp_host
    current_user.smtp_port = settings_data.smtp_port
    current_user.smtp_user = settings_data.smtp_user
    current_user.smtp_password = settings_data.smtp_password
    current_user.smtp_from_name = settings_data.smtp_from_name
    current_user.smtp_use_tls = settings_data.smtp_use_tls
    await db.commit()
    return {"success": True, "message": "SMTP outreach credentials updated successfully."}

@router.post("/me/smtp/test")
async def test_smtp_settings(
    settings_data: SMTPSettingsUpdate,
    current_user: User = Depends(get_current_user)
):
    import aiosmtplib
    if not settings_data.smtp_host or not settings_data.smtp_user or not settings_data.smtp_password:
        raise HTTPException(status_code=400, detail="Host, username/email, and password are all required to test SMTP.")

    try:
        smtp = aiosmtplib.SMTP(
            hostname=settings_data.smtp_host,
            port=settings_data.smtp_port or 587,
            start_tls=settings_data.smtp_use_tls,
            timeout=10
        )
        await smtp.connect()
        await smtp.login(settings_data.smtp_user, settings_data.smtp_password)
        await smtp.quit()
        return {"success": True, "message": f"SMTP handshake & authentication successful with {settings_data.smtp_host}!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SMTP Connection Failed: {str(e)}")


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.models.user import User
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
            target_field="AI/ML for Construction & Infrastructure Systems",
            current_degree="MSc Project & Infrastructure Management (Brunel, Merit) | B.E. Civil Engineering (Honours)",
            research_interests="AI/ML for Construction & Infrastructure Systems, Predictive Construction Risk Analytics, Cost & Schedule Forecasting Models, AI-Assisted Project Monitoring, BIM + AI / Digital Construction, Data-Driven Project Controls, Human-AI Decision Support, Sustainable & Resilient Infrastructure",
            cv_summary="AI/ML-oriented civil engineer and MSc graduate (Project & Infrastructure Management, Brunel University London, Merit) working at the intersection of machine learning, construction project controls, and infrastructure decision-making. Applied Python/Pandas data pipelines and supervised learning models (Random Forest, Decision Trees, Linear Regression) to construction schedule, cost, and resource data. Industry experience in construction, BIM (AutoCAD, Revit, STAAD Pro), peer-reviewed publications on waste materials/concrete, and national Best Paper Award."
        )
        db.add(user)
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
            "smtp_configured": bool(user.smtp_host and user.smtp_user)
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return {
        **current_user.__dict__,
        "smtp_configured": bool(current_user.smtp_host and current_user.smtp_user)
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
        "smtp_configured": bool(current_user.smtp_host and current_user.smtp_user)
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


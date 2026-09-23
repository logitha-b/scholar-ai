from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models.user import User, StudentProfile
from app.models.schemas import UserRegister, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    # create empty profile for students
    if data.role == "student":
        profile = StudentProfile(
            user_id=user.id,
            college=data.college,
            class_level=data.class_level,
        )
        db.add(profile)
        db.commit()
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer",
            "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}

@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")
    if not user.is_active:
        raise HTTPException(403, "Account is deactivated")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer",
            "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = current_user.profile
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "language": current_user.language,
        "college": profile.college if profile else None,
        "class_level": profile.class_level if profile else None,
        "stream": profile.stream if profile else None,
        "learning_style": profile.learning_style if profile else None,
        "daily_study_hours": profile.daily_study_hours if profile else 3.0,
        "subjects": profile.subjects_json if profile else [],
        "streak": profile.streak if profile else 0,
        "total_questions_solved": profile.total_questions_solved if profile else 0,
        "avg_score": profile.avg_score if profile else 0.0,
    }

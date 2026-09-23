from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime

# ── Auth ──────────────────────────────────────────────────────────────────────
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "student"          # "student" | "admin"
    college: Optional[str] = None
    class_level: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

# ── Profile ───────────────────────────────────────────────────────────────────
class SubjectScore(BaseModel):
    name: str
    score: float

class ProfileUpdate(BaseModel):
    college: Optional[str] = None
    class_level: Optional[str] = None
    stream: Optional[str] = None
    learning_style: Optional[str] = None
    daily_study_hours: Optional[float] = None
    subjects: Optional[List[SubjectScore]] = None
    language: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    language: str
    college: Optional[str]
    class_level: Optional[str]
    stream: Optional[str]
    learning_style: Optional[str]
    daily_study_hours: float
    subjects: Optional[List[dict]]
    streak: int
    total_questions_solved: int
    avg_score: float

    class Config:
        from_attributes = True

# ── Material ──────────────────────────────────────────────────────────────────
class MaterialResponse(BaseModel):
    id: int
    filename: str
    original_name: str
    file_type: str
    uploaded_at: datetime
    topic_analysis: Optional[Any]

    class Config:
        from_attributes = True

# ── AI Requests ───────────────────────────────────────────────────────────────
class NoteRequest(BaseModel):
    topic: str
    material_id: Optional[int] = None
    language: str = "en"

class FlashcardRequest(BaseModel):
    material_id: int           # generate from uploaded material
    count: int = 15            # 10-15 cards

class QARequest(BaseModel):
    material_id: int
    count: int = 10
    language: str = "en"

class DoubtRequest(BaseModel):
    question: str
    material_id: Optional[int] = None
    language: str = "en"

class SpeakingFeedbackRequest(BaseModel):
    transcript: str
    topic: str
    language: str = "en"

class WritingFeedbackRequest(BaseModel):
    text: str
    mode: str = "essay"
    language: str = "en"

class ResumeRequest(BaseModel):
    resume_text: str

class InterviewSimulateRequest(BaseModel):
    company_name: str
    round_type: str = "technical"
    difficulty: str = "medium"
    resume_text: str = ""

class StudyPlanRequest(BaseModel):
    subjects: List[SubjectScore]
    learning_style: str
    daily_hours: float
    language: str = "en"
    material_id: Optional[int] = None


# ── Test ──────────────────────────────────────────────────────────────────────
class SaveTestResult(BaseModel):
    topic: str
    total_questions: int
    correct: int
    score_pct: float

# ── Admin ─────────────────────────────────────────────────────────────────────
class AnnouncementCreate(BaseModel):
    title: str
    content: str

class AnnouncementResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class InterviewGradeRequest(BaseModel):
    questions: List[dict]
    answers: dict

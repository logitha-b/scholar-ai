from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="student")          # "student" | "admin"
    language = Column(String(10), default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    # relationships
    profile = relationship("StudentProfile", back_populates="user", uselist=False)
    materials = relationship("Material", back_populates="user")
    sessions = relationship("StudySession", back_populates="user")
    test_results = relationship("TestResult", back_populates="user")

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    college = Column(String(200))
    class_level = Column(String(50))          # "school_12", "college_1", etc.
    stream = Column(String(100))              # "Science", "Commerce", "Arts"
    learning_style = Column(String(50))
    daily_study_hours = Column(Float, default=3.0)
    subjects_json = Column(JSON)              # [{"name":"Maths","score":72}]
    streak = Column(Integer, default=0)
    total_questions_solved = Column(Integer, default=0)
    avg_score = Column(Float, default=0.0)
    user = relationship("User", back_populates="profile")

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String(255))
    original_name = Column(String(255))
    file_type = Column(String(50))            # "marksheet" | "study_material"
    extracted_text = Column(Text)
    topic_analysis = Column(JSON)             # AI-analyzed topics with weights
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="materials")

class StudyPlan(Base):
    __tablename__ = "study_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_text = Column(Text)
    weekly_schedule = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=True)
    topic = Column(String(200))
    question = Column(Text)
    answer = Column(Text)
    difficulty = Column(String(20), default="medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    module = Column(String(50))
    duration_minutes = Column(Integer)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="sessions")

class TestResult(Base):
    __tablename__ = "test_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String(200))
    total_questions = Column(Integer)
    correct = Column(Integer)
    score_pct = Column(Float)
    taken_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="test_results")

class AdminAnnouncement(Base):
    __tablename__ = "admin_announcements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300))
    content = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

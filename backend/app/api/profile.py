from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, StudentProfile, StudySession, TestResult
from app.models.schemas import ProfileUpdate, SaveTestResult
from sqlalchemy import func

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.put("/update")
def update_profile(data: ProfileUpdate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if data.language:
        current_user.language = data.language
        db.add(current_user)

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)

    if data.college is not None:     profile.college = data.college
    if data.class_level is not None: profile.class_level = data.class_level
    if data.stream is not None:      profile.stream = data.stream
    if data.learning_style is not None: profile.learning_style = data.learning_style
    if data.daily_study_hours is not None: profile.daily_study_hours = data.daily_study_hours
    if data.subjects is not None:
        profile.subjects_json = [s.dict() for s in data.subjects]
    db.commit()
    return {"message": "Profile updated"}

@router.post("/test-result")
def save_test_result(data: SaveTestResult, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    result = TestResult(
        user_id=current_user.id, topic=data.topic,
        total_questions=data.total_questions, correct=data.correct,
        score_pct=data.score_pct,
    )
    db.add(result)
    # update profile stats
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if profile:
        profile.total_questions_solved = (profile.total_questions_solved or 0) + data.total_questions
        all_scores = db.query(func.avg(TestResult.score_pct)).filter(TestResult.user_id == current_user.id).scalar()
        profile.avg_score = round(float(all_scores or 0), 1)
    db.commit()
    return {"message": "Saved"}

@router.post("/session")
def log_session(module: str, duration_minutes: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    session = StudySession(user_id=current_user.id, module=module, duration_minutes=duration_minutes)
    db.add(session)
    # update streak
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if profile:
        profile.streak = (profile.streak or 0) + 1
    db.commit()
    return {"message": "Session logged"}

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    recent_tests = db.query(TestResult).filter(TestResult.user_id == current_user.id)\
                     .order_by(TestResult.taken_at.desc()).limit(5).all()
    weekly_sessions = db.query(StudySession).filter(StudySession.user_id == current_user.id)\
                         .order_by(StudySession.date.desc()).limit(7).all()
                         
    # Fetch today's dynamic schedule from active StudyPlan
    from app.models.user import StudyPlan
    import datetime
    
    plan = db.query(StudyPlan).filter(StudyPlan.user_id == current_user.id, StudyPlan.is_active == True)\
             .order_by(StudyPlan.created_at.desc()).first()
             
    today_tasks = []
    if plan and plan.weekly_schedule:
        day_name = datetime.datetime.now().strftime("%A")
        schedule = plan.weekly_schedule.get("weekly_plan", {})
        
        # Check first week tasks for today
        week1 = schedule.get("week1", {})
        today_tasks = week1.get(day_name, [])
        if not today_tasks:
            # Fallback to check other weeks or other days if today is not scheduled
            for week_key in ["week1", "week2", "week3", "week4"]:
                week_sched = schedule.get(week_key, {})
                day_tasks = week_sched.get(day_name, [])
                if day_tasks:
                    today_tasks = day_tasks
                    break
            
            # Fallback to any day that has tasks if still empty
            if not today_tasks:
                for day, tasks in week1.items():
                    if tasks:
                        today_tasks = tasks
                        break
                        
        # Ensure all tasks have 'done' key
        new_tasks = []
        for task in today_tasks:
            new_task = dict(task)
            new_task["done"] = False
            new_tasks.append(new_task)
        today_tasks = new_tasks

    return {
        "profile": {
            "streak": profile.streak if profile else 0,
            "total_questions_solved": profile.total_questions_solved if profile else 0,
            "avg_score": profile.avg_score if profile else 0,
            "subjects": profile.subjects_json if profile else [],
        },
        "recent_tests": [
            {"topic": t.topic, "score_pct": t.score_pct, "correct": t.correct,
             "total": t.total_questions, "date": t.taken_at.isoformat()} for t in recent_tests
        ],
        "weekly_study": [
            {"module": s.module, "minutes": s.duration_minutes, "date": s.date.isoformat()}
            for s in weekly_sessions
        ],
        "today_tasks": today_tasks or [
            { "time": "9:00 AM", "subject": "Mathematics", "topic": "Calculus – Integration", "duration": "1.5h", "done": True },
            { "time": "11:00 AM", "subject": "Physics", "topic": "Electrostatics PYQs", "duration": "1h", "done": True },
            { "time": "2:00 PM", "subject": "Chemistry", "topic": "Organic Reactions", "duration": "1.5h", "done": False },
            { "time": "4:00 PM", "subject": "Aptitude", "topic": "Time & Work Practice", "duration": "45m", "done": False },
            { "time": "6:00 PM", "subject": "Communication", "topic": "Speaking Practice", "duration": "30m", "done": False }
        ]
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.user import User, StudentProfile, TestResult, Material, AdminAnnouncement
from app.models.schemas import AnnouncementCreate
from sqlalchemy import func

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/stats")
def admin_stats(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    total_students = db.query(User).filter(User.role == "student").count()
    total_admins = db.query(User).filter(User.role == "admin").count()
    total_materials = db.query(Material).count()
    total_tests = db.query(TestResult).count()
    avg_score = db.query(func.avg(TestResult.score_pct)).scalar() or 0
    return {
        "total_students": total_students,
        "total_admins": total_admins,
        "total_materials_uploaded": total_materials,
        "total_tests_taken": total_tests,
        "platform_avg_score": round(float(avg_score), 1),
    }

@router.get("/students")
def get_all_students(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    students = db.query(User).filter(User.role == "student").all()
    result = []
    for s in students:
        profile = s.profile
        result.append({
            "id": s.id, "name": s.name, "email": s.email,
            "is_active": s.is_active, "created_at": s.created_at.isoformat(),
            "college": profile.college if profile else None,
            "class_level": profile.class_level if profile else None,
            "streak": profile.streak if profile else 0,
            "questions_solved": profile.total_questions_solved if profile else 0,
            "avg_score": profile.avg_score if profile else 0,
        })
    return result

@router.put("/students/{user_id}/toggle")
def toggle_student(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.is_active = not user.is_active
    db.commit()
    return {"is_active": user.is_active}

@router.delete("/students/{user_id}")
def delete_student(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@router.get("/announcements")
def get_announcements(db: Session = Depends(get_db)):
    anns = db.query(AdminAnnouncement).filter(AdminAnnouncement.is_active == True)\
              .order_by(AdminAnnouncement.created_at.desc()).limit(10).all()
    return [{"id": a.id, "title": a.title, "content": a.content,
             "created_at": a.created_at.isoformat()} for a in anns]

@router.post("/announcements")
def create_announcement(data: AnnouncementCreate, db: Session = Depends(get_db),
                        admin=Depends(get_current_admin)):
    ann = AdminAnnouncement(title=data.title, content=data.content, created_by=admin.id)
    db.add(ann); db.commit(); db.refresh(ann)
    return {"id": ann.id, "message": "Announcement created"}

@router.delete("/announcements/{ann_id}")
def delete_announcement(ann_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    ann = db.query(AdminAnnouncement).filter(AdminAnnouncement.id == ann_id).first()
    if ann:
        ann.is_active = False
        db.commit()
    return {"message": "Deleted"}

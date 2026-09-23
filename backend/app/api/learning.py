from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, Material, StudyPlan, Flashcard
from app.models.schemas import (NoteRequest, FlashcardRequest, QARequest,
                                 DoubtRequest, StudyPlanRequest, SaveTestResult)
from app.services import file_service, ai_service

router = APIRouter(prefix="/api/learning", tags=["learning"])


# ── Upload Marksheet ──────────────────────────────────────────────────────────
@router.post("/upload/marksheet")
async def upload_marksheet(file: UploadFile = File(...),
                           db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    meta = await file_service.save_upload(file, subdirectory=f"user_{current_user.id}")
    text = file_service.extract_text(meta["file_path"], meta["extension"])
    subjects = ai_service.parse_marksheet_with_ai(meta["file_path"], meta["extension"], text)

    material = Material(
        user_id=current_user.id,
        filename=meta["filename"],
        original_name=meta["original_name"],
        file_type="marksheet",
        extracted_text=text,
        topic_analysis=subjects,
    )
    db.add(material); db.commit(); db.refresh(material)

    # AI analysis
    analysis = ai_service.analyse_marksheet(text, subjects, current_user.language)
    return {
        "material_id": material.id,
        "subjects": subjects,
        "analysis": analysis,
    }


# ── Upload Study Material ──────────────────────────────────────────────────────
@router.post("/upload/material")
async def upload_material(file: UploadFile = File(...),
                          db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    meta = await file_service.save_upload(file, subdirectory=f"user_{current_user.id}")
    text = file_service.extract_text(meta["file_path"], meta["extension"])
    topics = ai_service.analyse_topics_from_material(text)

    material = Material(
        user_id=current_user.id,
        filename=meta["filename"],
        original_name=meta["original_name"],
        file_type="study_material",
        extracted_text=text,
        topic_analysis=topics,
    )
    db.add(material); db.commit(); db.refresh(material)
    return {
        "material_id": material.id,
        "original_name": meta["original_name"],
        "topics": topics,
    }


# ── List user's materials ─────────────────────────────────────────────────────
@router.get("/materials")
def get_materials(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    mats = db.query(Material).filter(Material.user_id == current_user.id).all()
    return [{"id": m.id, "original_name": m.original_name,
             "file_type": m.file_type, "topics": m.topic_analysis,
             "uploaded_at": m.uploaded_at.isoformat()} for m in mats]


# ── Generate Study Plan ───────────────────────────────────────────────────────
@router.post("/study-plan")
def generate_plan(data: StudyPlanRequest, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    material_text = ""
    material_topics = []
    if data.material_id:
        mat = db.query(Material).filter(Material.id == data.material_id,
                                        Material.user_id == current_user.id).first()
        if mat:
            material_text = mat.extracted_text or ""
            material_topics = mat.topic_analysis or []

    plan = ai_service.generate_study_plan(
        [s.dict() for s in data.subjects],
        data.learning_style, data.daily_hours, data.language,
        material_text=material_text, material_topics=material_topics
    )
    db_plan = StudyPlan(user_id=current_user.id,
                        plan_text=str(plan.get("tips", "")),
                        weekly_schedule=plan)
    db.add(db_plan); db.commit()
    return plan



# ── AI Notes ─────────────────────────────────────────────────────────────────
@router.post("/notes")
def generate_notes(data: NoteRequest, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    material_text = ""
    if data.material_id:
        mat = db.query(Material).filter(Material.id == data.material_id,
                                        Material.user_id == current_user.id).first()
        if mat:
            material_text = mat.extracted_text or ""
    notes = ai_service.generate_notes(data.topic, material_text, data.language)
    return {"notes": notes}


# ── Flashcards from Uploaded Material ─────────────────────────────────────────
@router.post("/flashcards")
def generate_flashcards(data: FlashcardRequest, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    mat = db.query(Material).filter(Material.id == data.material_id,
                                    Material.user_id == current_user.id).first()
    if not mat:
        raise HTTPException(404, "Material not found")

    cards = ai_service.generate_flashcards_from_material(
        mat.extracted_text or "", count=min(data.count, 15)
    )
    # save to DB
    db_cards = []
    for c in cards:
        fc = Flashcard(user_id=current_user.id, material_id=mat.id,
                       topic=c.get("topic", ""), question=c.get("question", ""),
                       answer=c.get("answer", ""), difficulty=c.get("difficulty", "medium"))
        db.add(fc)
        db_cards.append(c)
    db.commit()
    return {"flashcards": db_cards, "count": len(db_cards)}


# ── Get saved flashcards ───────────────────────────────────────────────────────
@router.get("/flashcards/{material_id}")
def get_flashcards(material_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    cards = db.query(Flashcard).filter(Flashcard.user_id == current_user.id,
                                       Flashcard.material_id == material_id).all()
    return [{"id": c.id, "topic": c.topic, "question": c.question,
             "answer": c.answer, "difficulty": c.difficulty} for c in cards]


# ── Q&A from Material ─────────────────────────────────────────────────────────
@router.post("/qa")
def generate_qa(data: QARequest, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    mat = db.query(Material).filter(Material.id == data.material_id,
                                    Material.user_id == current_user.id).first()
    if not mat:
        raise HTTPException(404, "Material not found")
    questions = ai_service.generate_qa_from_material(
        mat.extracted_text or "", data.count, data.language
    )
    return {"questions": questions, "count": len(questions)}


# ── Doubt Solver ──────────────────────────────────────────────────────────────
@router.post("/doubt")
def solve_doubt(data: DoubtRequest, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    material_text = ""
    if data.material_id:
        mat = db.query(Material).filter(Material.id == data.material_id,
                                        Material.user_id == current_user.id).first()
        if mat:
            material_text = mat.extracted_text or ""
    answer = ai_service.solve_doubt(data.question, material_text, data.language)
    return {"answer": answer}


# ── Mock Test ─────────────────────────────────────────────────────────────────
@router.post("/mock-test")
def generate_mock_test(material_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    mat = db.query(Material).filter(Material.id == material_id,
                                    Material.user_id == current_user.id).first()
    if not mat:
        raise HTTPException(404, "Material not found")
    questions = ai_service.generate_qa_from_material(mat.extracted_text or "", count=10)
    return {"questions": questions}


# ── Save Test Result ──────────────────────────────────────────────────────────
@router.post("/test-result")
def save_result(data: SaveTestResult, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    from app.models.user import TestResult
    result = TestResult(user_id=current_user.id, topic=data.topic,
                        total_questions=data.total_questions,
                        correct=data.correct, score_pct=data.score_pct)
    db.add(result); db.commit()
    return {"message": "Result saved"}

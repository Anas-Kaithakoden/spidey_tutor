import logging
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Material
from app.schemas import CreateStudyPlan, StudyPlanOut
from app.services.study_plan import generate_study_plan

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/study-plan", tags=["study-plan"])


@router.post("", response_model=StudyPlanOut)
def create_study_plan(payload: CreateStudyPlan, db: Session = Depends(get_db)):
    # Get syllabus text
    syllabus = (payload.syllabus or "").strip()
    if payload.material_id is not None:
        mat = db.get(Material, payload.material_id)
        if not mat:
            raise HTTPException(status_code=404, detail="Material not found.")
        # if both provided, combine; else use material
        if syllabus:
            syllabus = f"{mat.content}\n\nAdditional syllabus:\n{syllabus}"
        else:
            syllabus = mat.content

    if not syllabus or len(syllabus) < 10:
        raise HTTPException(status_code=422, detail="Syllabus too short. Provide at least 10 characters or a material.")

    try:
        exam_d = date.fromisoformat(payload.exam_date)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid exam_date, use YYYY-MM-DD")
    days_left = (exam_d - date.today()).days
    if days_left <= 0:
        raise HTTPException(status_code=422, detail="exam_date must be a future date")

    generated_by, data = generate_study_plan(
        syllabus=syllabus,
        exam_date=payload.exam_date,
        daily_hours=payload.daily_hours,
        provider=payload.provider,
        model_name=payload.model_name,
        language=payload.language,
    )

    # data has plan + tips
    plan = data.get("plan", [])
    tips = data.get("tips", [])

    return StudyPlanOut(
        exam_date=payload.exam_date,
        days_left=days_left,
        daily_hours=payload.daily_hours,
        total_topics=len(plan),
        plan=plan,
        tips=tips,
        generated_by=generated_by,
        provider=payload.provider,
        model_name=payload.model_name or settings.gemini_model,
        language=payload.language,
    )

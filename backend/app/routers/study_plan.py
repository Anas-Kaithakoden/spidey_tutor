import logging
from datetime import date

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Material
from app.schemas import CreateStudyPlan, StudyPlanOut
from app.services.pdf import extract_pdf_text
from app.services.study_plan import generate_study_plan

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/study-plan", tags=["study-plan"])

MAX_PDF_BYTES = 15 * 1024 * 1024


def _validate_exam_date(exam_date: str) -> int:
    try:
        exam_d = date.fromisoformat(exam_date)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid exam_date, use YYYY-MM-DD")
    days_left = (exam_d - date.today()).days
    if days_left <= 0:
        raise HTTPException(status_code=422, detail="exam_date must be a future date")
    return days_left


def _build_plan_out(
    syllabus: str,
    exam_date: str,
    daily_hours: int,
    provider: str,
    model_name: str,
    language: str,
) -> StudyPlanOut:
    exam_d = date.fromisoformat(exam_date)
    days_left = (exam_d - date.today()).days

    generated_by, data = generate_study_plan(
        syllabus=syllabus,
        exam_date=exam_date,
        daily_hours=daily_hours,
        provider=provider,
        model_name=model_name,
        language=language,
    )

    # data has plan + tips
    plan = data.get("plan", [])
    tips = data.get("tips", [])

    return StudyPlanOut(
        exam_date=exam_date,
        days_left=days_left,
        daily_hours=daily_hours,
        total_topics=len(plan),
        plan=plan,
        tips=tips,
        generated_by=generated_by,
        provider=provider,
        model_name=model_name or settings.gemini_model,
        language=language,
    )


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

    _validate_exam_date(payload.exam_date)

    return _build_plan_out(
        syllabus=syllabus,
        exam_date=payload.exam_date,
        daily_hours=payload.daily_hours,
        provider=payload.provider,
        model_name=payload.model_name,
        language=payload.language,
    )


@router.post("/pdf", response_model=StudyPlanOut)
def create_study_plan_from_pdf(
    file: UploadFile = File(...),
    exam_date: str = Form(...),
    daily_hours: int = Form(3),
    provider: str = Form("gemini"),
    model_name: str = Form(""),
    language: str = Form("en"),
    syllabus: str = Form(""),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    data = file.file.read()
    if len(data) > MAX_PDF_BYTES:
        raise HTTPException(status_code=413, detail="PDF too large (max 15 MB).")

    try:
        content = extract_pdf_text(data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    extra = (syllabus or "").strip()
    if extra:
        content = f"{content}\n\nAdditional syllabus:\n{extra}"

    if not content or len(content) < 10:
        raise HTTPException(status_code=422, detail="No extractable syllabus text found in this PDF.")

    _validate_exam_date(exam_date)

    return _build_plan_out(
        syllabus=content,
        exam_date=exam_date,
        daily_hours=daily_hours,
        provider=provider,
        model_name=model_name,
        language=language,
    )

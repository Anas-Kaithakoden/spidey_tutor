from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Exam, ExamAttempt, ExamEvaluation, ExamQuestion, Material
from app.schemas import (
    CreateExam,
    ExamAnswerIn,
    ExamOut,
    ExamQuestionBrief,
    ExamQuestionReview,
    ExamResultOut,
    SubmitExam,
)
from app.services.exam import (
    evaluate_exam as service_evaluate,
    evaluation_criteria,
    generate_exam as service_generate,
)

router = APIRouter(prefix="/api/exams", tags=["exams"])


def _question_dict(q: ExamQuestion) -> dict:
    return {
        "id": q.id,
        "question_type": q.question_type,
        "question": q.question,
        "options": q.options,
        "correct_answer": q.correct_answer,
        "accepted_answer": q.accepted_answer,
        "key_points": q.key_points or [],
        "explanation": q.explanation,
        "max_score": q.max_score,
    }


def _exam_out(exam: Exam) -> ExamOut:
    return ExamOut(
        id=exam.id,
        material_id=exam.material_id,
        title=exam.title,
        difficulty=exam.difficulty,
        question_count=exam.question_count,
        duration_minutes=exam.duration_minutes,
        generated_by=exam.generated_by,
        provider=exam.provider,
        model_name=exam.model_name,
        questions=[
            ExamQuestionBrief(
                id=q.id,
                question_type=q.question_type,
                question=q.question,
                options=q.options,
                max_score=q.max_score,
            )
            for q in exam.questions
        ],
    )


def _result_out(
    exam: Exam, attempt: ExamAttempt, ev: ExamEvaluation
) -> ExamResultOut:
    reviews = [ExamQuestionReview(**rv) for rv in (ev.question_reviews or [])]
    return ExamResultOut(
        result_id=ev.id,
        exam_id=exam.id,
        attempt_id=attempt.id,
        total_score=ev.total_score,
        max_score=ev.max_score,
        percentage=ev.percentage,
        summary=ev.summary,
        strengths=ev.strengths or [],
        weak_areas=ev.weak_areas or [],
        topics_to_improve=ev.topics_to_improve or [],
        recommendations=ev.recommendations or [],
        reviews=reviews,
        grading_method=ev.grading_method,
        generated_by=exam.generated_by,
        criteria_used=ev.criteria or {},
    )


def _sanitize_answers(
    questions: list[ExamQuestion], payload_items: list[ExamAnswerIn]
) -> dict[int, dict]:
    """Map submitted answers onto question ids; drop invalid/incomplete ones."""
    by_id: dict[int, dict] = {}
    for item in payload_items:
        question = next(
            (q for q in questions if q.id == item.question_id), None
        )
        if question is None:
            continue
        if question.question_type == "mcq":
            option = item.option
            options = question.options or []
            if not isinstance(option, int) or not (0 <= option < len(options)):
                continue
            by_id[question.id] = {"text": None, "option": option}
        else:
            text = (item.text or "").strip()
            if not text:
                continue
            by_id[question.id] = {"text": text, "option": None}
    return by_id


@router.post("", response_model=ExamOut, status_code=201)
def create_exam(payload: CreateExam, db: Session = Depends(get_db)):
    material = db.get(Material, payload.material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")

    generated_by, questions, warning = service_generate(
        material.content,
        payload.difficulty,
        payload.question_count,
        provider=payload.provider,
        model_name=payload.model_name,
    )

    title = (payload.title or f"Exam on {material.title}").strip()
    exam = Exam(
        material_id=material.id,
        title=title,
        difficulty=payload.difficulty,
        question_count=len(questions),
        duration_minutes=payload.duration_minutes,
        generated_by=generated_by,
        provider=payload.provider,
        model_name=payload.model_name,
    )
    db.add(exam)
    db.flush()

    for idx, q in enumerate(questions):
        db.add(
            ExamQuestion(
                exam_id=exam.id,
                question_type=q["question_type"],
                question=q["question"],
                options=q["options"],
                correct_answer=q["correct_answer"],
                accepted_answer=q["accepted_answer"],
                key_points=q["key_points"],
                explanation=q["explanation"],
                max_score=q["max_score"],
                sort_order=idx,
            )
        )

    db.commit()
    db.refresh(exam)
    out = _exam_out(exam)
    out.warning = warning or None
    return out


@router.get("", response_model=list[ExamOut])
def list_exams(
    material_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Exam).order_by(
        Exam.created_at.desc(), Exam.id.desc()
    )
    if material_id is not None:
        query = query.filter(Exam.material_id == material_id)
    return [_exam_out(exam) for exam in query.all()]


@router.get("/{exam_id}", response_model=ExamOut)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.get(Exam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found.")
    return _exam_out(exam)


@router.post("/{exam_id}/submit", response_model=ExamResultOut)
def submit_exam(
    exam_id: int, payload: SubmitExam, db: Session = Depends(get_db)
):
    exam = db.get(Exam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found.")

    questions = sorted(exam.questions, key=lambda q: q.sort_order)
    answers_by_id = _sanitize_answers(questions, payload.answers)

    attempt = ExamAttempt(
        exam_id=exam.id,
        answers=[
            {
                "question_id": qid,
                "text": vals.get("text"),
                "option": vals.get("option"),
            }
            for qid, vals in sorted(answers_by_id.items())
        ],
        time_taken_seconds=payload.time_taken_seconds,
    )
    db.add(attempt)
    db.flush()

    criteria = payload.evaluation_criteria or evaluation_criteria()
    provider = payload.provider or exam.provider
    model_name = payload.model_name or exam.model_name

    grading_method, result, warning = service_evaluate(
        [_question_dict(q) for q in questions],
        answers_by_id,
        exam.material.content,
        provider=provider,
        model_name=model_name,
        criteria=criteria,
    )

    evaluation = ExamEvaluation(
        attempt_id=attempt.id,
        total_score=result["total_score"],
        max_score=result["max_score"],
        percentage=result["percentage"],
        summary=result["summary"],
        strengths=result["strengths"],
        weak_areas=result["weak_areas"],
        topics_to_improve=result.get("topics_to_improve", []),
        recommendations=result["recommendations"],
        question_reviews=result["reviews"],
        grading_method=grading_method,
        criteria=criteria,
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    db.refresh(attempt)

    out = _result_out(exam, attempt, evaluation)
    out.warning = warning or None
    return out


@router.get("/{exam_id}/result", response_model=ExamResultOut)
def get_latest_result(exam_id: int, db: Session = Depends(get_db)):
    exam = db.get(Exam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found.")

    row = (
        db.query(ExamEvaluation, ExamAttempt)
        .join(ExamAttempt, ExamEvaluation.attempt_id == ExamAttempt.id)
        .filter(ExamAttempt.exam_id == exam_id)
        .order_by(ExamAttempt.created_at.desc(), ExamAttempt.id.desc())
        .first()
    )
    if not row:
        raise HTTPException(
            status_code=404, detail="This exam has not been submitted yet."
        )
    evaluation, attempt = row
    return _result_out(exam, attempt, evaluation)
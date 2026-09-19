from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Material, Question, Quiz, QuizResult
from app.schemas import (
    CreateQuiz,
    QuestionBrief,
    QuestionReview,
    QuizOut,
    QuizResultOut,
    SubmitQuiz,
)
from app.services.ai import generate_quiz as ai_generate_quiz

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])


def _quiz_out(quiz: Quiz) -> QuizOut:
    return QuizOut(
        id=quiz.id,
        material_id=quiz.material_id,
        difficulty=quiz.difficulty,
        question_count=quiz.question_count,
        timer_enabled=quiz.timer_enabled,
        timer_minutes=quiz.timer_minutes,
        generated_by=quiz.generated_by,
        provider=quiz.provider,
        model_name=quiz.model_name,
        questions=[
            QuestionBrief(id=q.id, question=q.question, options=q.options)
            for q in quiz.questions
        ],
    )


@router.post("", response_model=QuizOut, status_code=201)
def create_quiz(payload: CreateQuiz, db: Session = Depends(get_db)):
    material = db.get(Material, payload.material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")

    generated_by, questions, warning = ai_generate_quiz(
        material.content,
        payload.difficulty,
        payload.question_count,
        provider=payload.provider,
        model_name=payload.model_name,
    )

    quiz = Quiz(
        material_id=material.id,
        difficulty=payload.difficulty,
        question_count=len(questions),
        timer_enabled=payload.timer_enabled,
        timer_minutes=payload.timer_minutes,
        generated_by=generated_by,
        provider=payload.provider,
        model_name=payload.model_name,
    )
    db.add(quiz)
    db.flush()

    for idx, q in enumerate(questions):
        db.add(
            Question(
                quiz_id=quiz.id,
                question=q["question"],
                options=q["options"],
                correct_answer=q["correct_answer"],
                explanation=q["explanation"],
                sort_order=idx,
            )
        )

    db.commit()
    db.refresh(quiz)
    out = _quiz_out(quiz)
    out.warning = warning or None
    return out


@router.get("/{quiz_id}", response_model=QuizOut)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")
    return _quiz_out(quiz)


@router.post("/{quiz_id}/submit", response_model=QuizResultOut)
def submit_quiz(
    quiz_id: int, payload: SubmitQuiz, db: Session = Depends(get_db)
):
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    questions = sorted(quiz.questions, key=lambda q: q.sort_order)
    total = len(questions)
    answers = payload.answers[:total]
    answers = [a if isinstance(a, int) else None for a in answers]
    while len(answers) < total:
        answers.append(None)

    score = sum(
        1 for a, q in zip(answers, questions) if a == q.correct_answer
    )
    percentage = round((score / total) * 100) if total else 0

    result = QuizResult(
        quiz_id=quiz.id,
        answers=answers,
        score=score,
        total=total,
        percentage=percentage,
        time_taken_seconds=payload.time_taken_seconds,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    reviews = []
    for user_answer, q in zip(answers, questions):
        reviews.append(
            QuestionReview(
                question=q.question,
                options=q.options,
                correct_answer=q.correct_answer,
                user_answer=user_answer,
                is_correct=user_answer == q.correct_answer,
                explanation=q.explanation,
            )
        )

    return QuizResultOut(
        result_id=result.id,
        quiz_id=quiz.id,
        score=score,
        total=total,
        percentage=percentage,
        answers=answers,
        generated_by=quiz.generated_by,
        reviews=reviews,
    )
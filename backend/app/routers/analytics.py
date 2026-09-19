from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Flashcard, Material, Quiz, QuizResult, StudyNote
from app.schemas import (
    AnalyticsOut,
    RecentActivity,
    ScoreTrendPoint,
    TopicPerformance,
)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("", response_model=AnalyticsOut)
def get_analytics(db: Session = Depends(get_db)):
    materials = db.query(Material).order_by(Material.created_at).all()
    flashcards = db.query(Flashcard).all()
    notes = db.query(StudyNote).all()
    results = (
        db.query(QuizResult)
        .join(Quiz, QuizResult.quiz_id == Quiz.id)
        .order_by(QuizResult.created_at.asc())
        .all()
    )

    material_map = {m.id: m for m in materials}
    quiz_map = {q.id: q for q in db.query(Quiz).all()}

    quizzes_completed = len(results)
    questions_answered = sum(r.total for r in results)
    correct_answers = sum(r.score for r in results)
    incorrect_answers = max(questions_answered - correct_answers, 0)
    average_score = (
        round(correct_answers / questions_answered * 100)
        if questions_answered
        else 0
    )
    best_score = max((r.percentage for r in results), default=None)
    flashcards_reviewed = sum(c.review_count for c in flashcards)
    study_sessions = quizzes_completed + flashcards_reviewed

    activity_dates: set[date] = {r.created_at.date() for r in results}
    activity_dates.update(c.created_at.date() for c in flashcards)
    activity_dates.update(n.created_at.date() for n in notes)
    activity_dates.update(m.created_at.date() for m in materials)
    days_studied = len(activity_dates)

    # Performance grouped by quiz material (the app's closest notion of topics)
    by_topic: dict[int, dict] = {}
    for r in results:
        material_id = quiz_map.get(r.quiz_id).material_id if quiz_map.get(r.quiz_id) else None
        if material_id is None:
            continue
        topic = by_topic.get(material_id)
        if topic is None:
            topic = {"quizzes_taken": 0, "questions_answered": 0, "correct": 0}
            by_topic[material_id] = topic
        topic["quizzes_taken"] += 1
        topic["questions_answered"] += r.total
        topic["correct"] += r.score

    topics = []
    for material_id, t in by_topic.items():
        avg = (
            round(t["correct"] / t["questions_answered"] * 100)
            if t["questions_answered"]
            else 0
        )
        material = material_map.get(material_id)
        topics.append(
            TopicPerformance(
                material_id=material_id,
                title=material.title if material else f"Material #{material_id}",
                quizzes_taken=t["quizzes_taken"],
                questions_answered=t["questions_answered"],
                correct=t["correct"],
                average_score=avg,
                needs_practice=avg < 70,
            )
        )
    topics.sort(key=lambda t: (t.average_score, t.title))

    score_trend = []
    for r in results:
        quiz = quiz_map.get(r.quiz_id)
        material = material_map.get(quiz.material_id) if quiz else None
        score_trend.append(
            ScoreTrendPoint(
                label=r.created_at.strftime("%b %d"),
                score=r.percentage,
                created_at=r.created_at,
                material_title=material.title if material else "Quiz",
            )
        )

    events: list[RecentActivity] = []
    for m in materials:
        events.append(
            RecentActivity(
                kind="material",
                title=m.title,
                detail="Added study material",
                material_id=m.id,
                created_at=m.created_at,
            )
        )
    for r in results:
        quiz = quiz_map.get(r.quiz_id)
        material = material_map.get(quiz.material_id) if quiz else None
        events.append(
            RecentActivity(
                kind="quiz",
                title=material.title if material else "Quiz",
                detail=f"Scored {r.percentage}% ({r.score}/{r.total})",
                material_id=material.id if material else None,
                created_at=r.created_at,
            )
        )
    decks: dict[int, list[Flashcard]] = {}
    for c in flashcards:
        decks.setdefault(c.material_id, []).append(c)
    for material_id, cards in decks.items():
        material = material_map.get(material_id)
        events.append(
            RecentActivity(
                kind="flashcards",
                title=material.title if material else "Flashcards",
                detail=f"{len(cards)} cards",
                material_id=material_id,
                created_at=max(c.created_at for c in cards),
            )
        )
    for n in notes:
        material = material_map.get(n.material_id)
        events.append(
            RecentActivity(
                kind="notes",
                title=material.title if material else "Study notes",
                detail="Generated study notes",
                material_id=n.material_id,
                created_at=n.created_at,
            )
        )
    events.sort(key=lambda e: e.created_at, reverse=True)

    return AnalyticsOut(
        has_activity=bool(results or flashcards),
        materials=len(materials),
        quizzes_completed=quizzes_completed,
        questions_answered=questions_answered,
        correct_answers=correct_answers,
        incorrect_answers=incorrect_answers,
        average_score=average_score,
        best_score=best_score,
        flashcards=len(flashcards),
        flashcards_reviewed=flashcards_reviewed,
        study_sessions=study_sessions,
        days_studied=days_studied,
        topics=topics,
        score_trend=score_trend,
        recent_activity=events[:8],
    )
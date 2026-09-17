from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    source_type: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    quizzes: Mapped[list["Quiz"]] = relationship(
        back_populates="material", cascade="all, delete-orphan"
    )
    flashcards: Mapped[list["Flashcard"]] = relationship(
        back_populates="material", cascade="all, delete-orphan"
    )


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"))
    difficulty: Mapped[str] = mapped_column(String(16))
    question_count: Mapped[int] = mapped_column(Integer)
    timer_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    timer_minutes: Mapped[int] = mapped_column(Integer, default=10)
    generated_by: Mapped[str] = mapped_column(String(8), default="mock")
    provider: Mapped[str] = mapped_column(String(16), default="gemini")
    model_name: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    material: Mapped[Material] = relationship(back_populates="quizzes")
    questions: Mapped[list["Question"]] = relationship(
        back_populates="quiz",
        cascade="all, delete-orphan",
        order_by="Question.sort_order",
    )
    results: Mapped[list["QuizResult"]] = relationship(
        back_populates="quiz", cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"))
    question: Mapped[str] = mapped_column(Text)
    options: Mapped[list] = mapped_column(JSON)
    correct_answer: Mapped[int] = mapped_column(Integer)
    explanation: Mapped[str] = mapped_column(Text, default="")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    quiz: Mapped[Quiz] = relationship(back_populates="questions")


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"))
    answers: Mapped[list] = mapped_column(JSON)
    score: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer)
    percentage: Mapped[int] = mapped_column(Integer)
    time_taken_seconds: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    quiz: Mapped[Quiz] = relationship(back_populates="results")


class Flashcard(Base):
    __tablename__ = "flashcards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"))
    front: Mapped[str] = mapped_column(Text)
    back: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    provider: Mapped[str] = mapped_column(String(16), default="gemini")
    model_name: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    material: Mapped[Material] = relationship(back_populates="flashcards")
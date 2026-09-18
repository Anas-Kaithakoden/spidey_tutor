from datetime import datetime

from pydantic import BaseModel, Field


class CreateMaterial(BaseModel):
    title: str | None = None
    text: str = Field(min_length=1)


class MaterialOut(BaseModel):
    id: int
    title: str
    content: str
    source_type: str
    char_count: int
    word_count: int
    created_at: datetime


class QuestionBrief(BaseModel):
    id: int
    question: str
    options: list[str]


class QuizOut(BaseModel):
    id: int
    material_id: int
    difficulty: str
    question_count: int
    timer_enabled: bool
    timer_minutes: int
    generated_by: str
    provider: str
    model_name: str
    questions: list[QuestionBrief]


class CreateQuiz(BaseModel):
    material_id: int
    difficulty: str = "medium"
    question_count: int = Field(default=5, ge=1, le=20)
    timer_enabled: bool = False
    timer_minutes: int = Field(default=10, ge=1, le=120)
    provider: str = "gemini"
    model_name: str = ""


class SubmitQuiz(BaseModel):
    answers: list[int | None]
    time_taken_seconds: int = 0


class QuestionReview(BaseModel):
    question: str
    options: list[str]
    correct_answer: int
    user_answer: int | None
    is_correct: bool
    explanation: str


class QuizResultOut(BaseModel):
    result_id: int
    quiz_id: int
    score: int
    total: int
    percentage: int
    answers: list[int | None]
    generated_by: str
    reviews: list[QuestionReview]


class CreateFlashcards(BaseModel):
    material_id: int
    provider: str = "gemini"
    model_name: str = ""


class FlashcardOut(BaseModel):
    id: int
    front: str
    back: str
    provider: str
    model_name: str


class CreateStudyNotes(BaseModel):
    material_id: int
    provider: str = "gemini"
    model_name: str = ""


class StudyNoteSection(BaseModel):
    heading: str
    content: str
    bullet_points: list[str] = []


class StudyNoteKeyConcept(BaseModel):
    term: str
    definition: str


class StudyNotesOut(BaseModel):
    id: int
    material_id: int
    title: str
    summary: str
    sections: list[StudyNoteSection]
    key_concepts: list[StudyNoteKeyConcept]
    generated_by: str
    provider: str
    model_name: str
    created_at: datetime


class ModelInfo(BaseModel):
    provider: str
    name: str
    label: str


class ModelsOut(BaseModel):
    providers: list[ModelInfo]


class HealthOut(BaseModel):
    status: str
    gemini_configured: bool
    database: str


class FlashcardReviewOut(BaseModel):
    id: int
    review_count: int


class TopicPerformance(BaseModel):
    material_id: int
    title: str
    quizzes_taken: int
    questions_answered: int
    correct: int
    average_score: int
    needs_practice: bool


class RecentActivity(BaseModel):
    kind: str
    title: str
    detail: str
    material_id: int | None
    created_at: datetime


class ScoreTrendPoint(BaseModel):
    label: str
    score: int
    created_at: datetime
    material_title: str


class AnalyticsOut(BaseModel):
    has_activity: bool
    materials: int
    quizzes_completed: int
    questions_answered: int
    correct_answers: int
    incorrect_answers: int
    average_score: int
    best_score: int | None
    flashcards: int
    flashcards_reviewed: int
    study_sessions: int
    days_studied: int
    topics: list[TopicPerformance]
    score_trend: list[ScoreTrendPoint]
    recent_activity: list[RecentActivity]
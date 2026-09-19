from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class CreateMaterial(BaseModel):
    title: str | None = None
    text: str = Field(min_length=1)


class MaterialOut(BaseModel):
    id: int
    title: str
    content: str
    source_type: str
    source_url: str | None = None
    char_count: int
    word_count: int
    created_at: datetime


class CreateYoutubeMaterial(BaseModel):
    url: str = Field(min_length=1)
    title: str | None = None


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
    warning: str | None = None


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
    language: str = "en"


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
    language: str = "en"
    created_at: datetime
    warning: str | None = None


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


class CreateAudioSummary(BaseModel):
    material_id: int
    provider: str = "gemini"
    model_name: str = ""
    voice_name: str = "Kore"
    language: str = "en"


class AudioSummaryOut(BaseModel):
    material_id: int
    summary_text: str
    audio_base64: str
    mime_type: str
    generated_by: str
    provider: str
    model_name: str


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


class ChatMessageOut(BaseModel):
    id: int
    material_id: int
    role: str
    content: str
    generated_by: str
    language: str = "en"
    created_at: datetime


class CreateChatMessage(BaseModel):
    material_id: int
    content: str = Field(min_length=1, max_length=4000)
    provider: str = "gemini"
    model_name: str = ""
    language: str = "en"

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be blank.")
        return v


class ChatReplyOut(BaseModel):
    user_message: ChatMessageOut
    assistant_message: ChatMessageOut
    warning: str | None = None


class CreateExam(BaseModel):
    material_id: int
    title: str | None = None
    difficulty: str = "medium"
    question_count: int = Field(default=10, ge=1, le=50)
    duration_minutes: int = Field(default=30, ge=1, le=240)
    provider: str = "gemini"
    model_name: str = ""


class ExamQuestionBrief(BaseModel):
    id: int
    question_type: str
    question: str
    options: list[str] | None = None
    max_score: int


class ExamOut(BaseModel):
    id: int
    material_id: int
    title: str
    difficulty: str
    question_count: int
    duration_minutes: int
    generated_by: str
    provider: str
    model_name: str
    questions: list[ExamQuestionBrief]
    warning: str | None = None


class ExamAnswerIn(BaseModel):
    question_id: int
    text: str | None = None
    option: int | None = None


class SubmitExam(BaseModel):
    answers: list[ExamAnswerIn] = []
    time_taken_seconds: int = 0
    # Optional grading model override (defaults to the exam's provider/model).
    provider: str | None = None
    model_name: str = ""
    evaluation_criteria: dict | None = None


class ExamQuestionReview(BaseModel):
    question_id: int
    question: str
    question_type: str
    user_answer: str | None
    expected_answer: str
    status: str  # correct | partial | incorrect | unanswered
    score: float
    max_score: int
    feedback: str
    improved_answer: str | None = None


class ExamResultOut(BaseModel):
    result_id: int
    exam_id: int
    attempt_id: int
    total_score: float
    max_score: int
    percentage: float
    summary: str
    strengths: list[str]
    weak_areas: list[str]
    topics_to_improve: list[str]
    recommendations: list[str]
    reviews: list[ExamQuestionReview]
    grading_method: str  # deterministic | hybrid | fallback
    generated_by: str
    criteria_used: dict
    warning: str | None = None


# ---------------------------------------------------------------------------
# Study Podcast
# ---------------------------------------------------------------------------

PodcastMode = Literal["learn", "revise", "exam_prep", "weak_topics"]

PODCAST_MODES = ("learn", "revise", "exam_prep", "weak_topics")
PODCAST_MAX_DURATION_MINUTES = 10


class CreatePodcast(BaseModel):
    material_id: int
    title: str | None = None
    mode: PodcastMode = "learn"
    duration_minutes: int = Field(default=5, ge=1, le=PODCAST_MAX_DURATION_MINUTES)
    focus_topic: str = ""
    provider: str = "gemini"
    model_name: str = ""

    @field_validator("focus_topic")
    @classmethod
    def focus_topic_trimmed(cls, v: str) -> str:
        return (v or "").strip()

    @field_validator("mode")
    @classmethod
    def mode_supported(cls, v: str) -> str:
        if v not in PODCAST_MODES:
            raise ValueError(
                f"Unsupported podcast mode '{v}'. Choose one of "
                + ", ".join(PODCAST_MODES)
                + "."
            )
        return v


class PodcastScriptLine(BaseModel):
    speaker: Literal["host_one", "host_two"]
    text: str

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Dialogue line cannot be blank.")
        return v


class PodcastEpisodeOut(BaseModel):
    id: int
    material_id: int
    material_title: str = ""
    title: str
    mode: str
    duration_minutes: int
    focus_topic: str = ""
    lines: list[PodcastScriptLine]
    generated_by: str  # ai | quick | mock
    provider: str
    model_name: str
    audio_status: str  # ready | unavailable | error
    has_audio: bool
    audio_url: str | None = None
    created_at: datetime
    warning: str | None = None


# ---------------------------------------------------------------------------
# Study Plan
# ---------------------------------------------------------------------------


class CreateStudyPlan(BaseModel):
    syllabus: str | None = None
    material_id: int | None = None
    exam_date: str = Field(description="ISO date YYYY-MM-DD")
    daily_hours: int = Field(default=3, ge=1, le=12)
    provider: str = "gemini"
    model_name: str = ""
    language: str = "en"

    @field_validator("exam_date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        from datetime import date

        try:
            d = date.fromisoformat(v)
        except Exception:
            raise ValueError("exam_date must be YYYY-MM-DD")
        if d <= date.today():
            raise ValueError("exam_date must be a future date")
        return v


class StudyPlanDay(BaseModel):
    day: int
    date: str
    topic: str
    tasks: list[str]
    focus: str
    duration_hours: float
    revision: bool = False


class StudyPlanOut(BaseModel):
    exam_date: str
    days_left: int
    daily_hours: int
    total_topics: int
    plan: list[StudyPlanDay]
    tips: list[str]
    generated_by: str
    provider: str
    model_name: str
    language: str

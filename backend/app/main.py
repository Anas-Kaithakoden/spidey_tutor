import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.models import Material  # noqa: F401 (ensure models are registered)
from app.routers import analytics, flashcards, materials, quizzes, study_notes
from app.schemas import HealthOut, ModelInfo, ModelsOut
from app.services import ollama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info(
        "Database ready (current backend = %s)",
        settings.database_url.split(":", 1)[0],
    )
    if not settings.gemini_api_key:
        logger.warning(
            "GEMINI_API_KEY is not set. AI features will fall back to mock data."
        )
    yield


app = FastAPI(title="Spidey Tutor API", version="1.0.0", lifespan=lifespan)

origins = [
    o.strip() for o in settings.cors_origins.split(",") if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(materials.router)
app.include_router(quizzes.router)
app.include_router(flashcards.router)
app.include_router(study_notes.router)
app.include_router(analytics.router)


@app.get("/api/health", response_model=HealthOut)
def health():
    return HealthOut(
        status="ok",
        gemini_configured=bool(settings.gemini_api_key),
        database=settings.database_url.split(":", 1)[0],
    )


@app.get("/api/models", response_model=ModelsOut)
def list_models():
    providers: list[ModelInfo] = []

    # Gemini
    if settings.gemini_api_key:
        providers.append(
            ModelInfo(provider="gemini", name=settings.gemini_model, label="Gemini")
        )
    else:
        providers.append(
            ModelInfo(
                provider="gemini",
                name=settings.gemini_model,
                label="Gemini (no API key)",
            )
        )

    # Ollama
    ollama_models = ollama.available_models()
    if ollama_models:
        providers.extend(
            ModelInfo(provider=m["provider"], name=m["name"], label=m["label"])
            for m in ollama_models
        )
    else:
        providers.append(
            ModelInfo(provider="ollama", name="qwen3:8b", label="Local (unreachable)")
        )

    # Quick — deterministic local generation, always available, no API call
    providers.append(
        ModelInfo(
            provider="quick",
            name="quick",
            label="Quick (deterministic, no AI)",
        )
    )

    return ModelsOut(providers=providers)
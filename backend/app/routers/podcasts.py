import logging
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import (
    Material,
    PodcastEpisode,
    Quiz,
    QuizResult,
)
from app.schemas import (
    CreatePodcast,
    PodcastEpisodeOut,
    PodcastScriptLine,
)
from app.services.audio import (
    podcast_duration_seconds,
    synthesize_podcast_audio,
)
from app.services.podcast import (
    generate_podcast_script,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/podcasts", tags=["podcasts"])


def _weak_topics_snapshot(db: Session) -> list[dict]:
    """Weak-topic performance snapshot (mirrors the analytics dashboard).

    Per-material quiz performance, filtered to topics the student is struggling
    with (average < 70%), weakest first. Only topics with real data appear —
    the podcast prompt is told never to invent performance facts.
    """
    results = (
        db.query(QuizResult)
        .join(Quiz, QuizResult.quiz_id == Quiz.id)
        .order_by(QuizResult.created_at.asc())
        .all()
    )
    quiz_map = {q.id: q for q in db.query(Quiz).all()}
    material_map = {m.id: m for m in db.query(Material).all()}

    by_topic: dict[int, dict] = {}
    for r in results:
        quiz = quiz_map.get(r.quiz_id)
        if quiz is None:
            continue
        topic = by_topic.setdefault(
            quiz.material_id, {"quizzes_taken": 0, "questions_answered": 0, "correct": 0}
        )
        topic["quizzes_taken"] += 1
        topic["questions_answered"] += r.total
        topic["correct"] += r.score

    snapshot = []
    for material_id, t in by_topic.items():
        average = (
            round(t["correct"] / t["questions_answered"] * 100)
            if t["questions_answered"]
            else 0
        )
        if average >= 70:
            continue
        material = material_map.get(material_id)
        snapshot.append(
            {
                "material_id": material_id,
                "title": material.title if material else f"Material #{material_id}",
                "average_score": average,
                "questions_answered": t["questions_answered"],
                "quizzes_taken": t["quizzes_taken"],
            }
        )
    snapshot.sort(key=lambda t: t["average_score"])
    return snapshot[:5]


def _episode_out(episode: PodcastEpisode, material: Material | None) -> PodcastEpisodeOut:
    lines = [PodcastScriptLine(**line) for line in (episode.lines or [])]
    return PodcastEpisodeOut(
        id=episode.id,
        material_id=episode.material_id,
        material_title=material.title if material else "",
        title=episode.title,
        mode=episode.mode,
        duration_minutes=episode.duration_minutes,
        focus_topic=episode.focus_topic,
        lines=lines,
        generated_by=episode.generated_by,
        provider=episode.provider,
        model_name=episode.model_name,
        audio_status=episode.audio_status,
        has_audio=episode.audio_status == "ready"
        and bool(episode.audio_path),
        audio_url=(
            f"/api/podcasts/{episode.id}/audio"
            if episode.audio_status == "ready" and episode.audio_path
            else None
        ),
        created_at=episode.created_at,
    )


def _confirm_audio_exists(episode: PodcastEpisode) -> None:
    if not episode.audio_path or not Path(episode.audio_path).is_file():
        raise HTTPException(status_code=404, detail="Episode audio not found.")


def _sync_audio(episode: PodcastEpisode) -> str:
    """Synthesize episode audio to disk. Returns a user-facing status note."""
    if not settings.gemini_api_key:
        episode.audio_status = "unavailable"
        return (
            "Audio unavailable — GEMINI_API_KEY is not set. The script is saved; "
            "add the key to backend/.env and retry audio synthesis."
        )

    try:
        mime_type, wav = synthesize_podcast_audio(
            episode.lines,
            voice_one=settings.podcast_voice_host_one,
            voice_two=settings.podcast_voice_host_two,
        )
    except Exception as exc:
        logger.exception(
            "Podcast TTS failed (episode=%s): %s", episode.id, exc
        )
        episode.audio_status = "error"
        return f"Audio generation failed: {exc}"

    media_dir = Path(settings.podcast_media_dir)
    if not media_dir.is_absolute():
        media_dir = Path.cwd() / media_dir
    media_dir.mkdir(parents=True, exist_ok=True)
    audio_path = media_dir / f"podcast_{episode.id}.wav"
    audio_path.write_bytes(wav)
    episode.audio_path = str(audio_path)
    episode.audio_status = "ready"
    note = f"Audio ready. Estimated duration ~{int(podcast_duration_seconds(wav) // 60)} min."
    return note


@router.post("", response_model=PodcastEpisodeOut, status_code=201)
def create_podcast(payload: CreatePodcast, db: Session = Depends(get_db)):
    material = db.get(Material, payload.material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")
    if not material.content or not material.content.strip():
        raise HTTPException(
            status_code=422,
            detail="Material has no usable content for a podcast.",
        )

    weak_topics = (
        _weak_topics_snapshot(db) if payload.mode == "weak_topics" else None
    )

    generated_by, script, warning = generate_podcast_script(
        material.content,
        mode=payload.mode,
        duration_minutes=payload.duration_minutes,
        provider=payload.provider,
        model_name=payload.model_name,
        focus_topic=payload.focus_topic,
        weak_topics=weak_topics,
    )

    title = (payload.title or script.get("title") or f"Podcast on {material.title}").strip()
    episode = PodcastEpisode(
        material_id=material.id,
        title=title,
        mode=payload.mode,
        duration_minutes=payload.duration_minutes,
        focus_topic=payload.focus_topic,
        lines=script["lines"],
        generated_by=generated_by,
        provider=payload.provider,
        model_name=payload.model_name,
        audio_status="unavailable",
    )
    db.add(episode)
    db.flush()

    audio_note = _sync_audio(episode)
    if audio_note and not warning:
        warning = audio_note

    db.commit()
    db.refresh(episode)
    out = _episode_out(episode, material)
    out.warning = warning or None
    return out


@router.get("", response_model=list[PodcastEpisodeOut])
def list_podcasts(
    material_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(PodcastEpisode).order_by(
        PodcastEpisode.created_at.desc(), PodcastEpisode.id.desc()
    )
    if material_id is not None:
        query = query.filter(PodcastEpisode.material_id == material_id)
    episodes = query.all()
    materials = {m.id: m for m in db.query(Material).all()}
    return [
        _episode_out(ep, materials.get(ep.material_id)) for ep in episodes
    ]


@router.get("/{episode_id}", response_model=PodcastEpisodeOut)
def get_podcast(episode_id: int, db: Session = Depends(get_db)):
    episode = db.get(PodcastEpisode, episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Podcast episode not found.")
    material = db.get(Material, episode.material_id)
    return _episode_out(episode, material)


@router.delete("/{episode_id}", status_code=204)
def delete_podcast(episode_id: int, db: Session = Depends(get_db)):
    episode = db.get(PodcastEpisode, episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Podcast episode not found.")
    if episode.audio_path:
        try:
            Path(episode.audio_path).unlink(missing_ok=True)
        except OSError:
            logger.warning("Could not remove audio file %s", episode.audio_path)
    db.delete(episode)
    db.commit()


@router.get("/{episode_id}/audio")
def get_podcast_audio(episode_id: int, db: Session = Depends(get_db)):
    episode = db.get(PodcastEpisode, episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Podcast episode not found.")
    _confirm_audio_exists(episode)
    return FileResponse(
        episode.audio_path,
        media_type="audio/wav",
        filename=f"podcast_{episode_id}.wav",
    )


@router.post("/{episode_id}/audio", response_model=PodcastEpisodeOut)
def regenerate_podcast_audio(episode_id: int, db: Session = Depends(get_db)):
    """Retry synthesis for an existing script-only episode (e.g. key added later)."""
    episode = db.get(PodcastEpisode, episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Podcast episode not found.")
    if not episode.lines:
        raise HTTPException(
            status_code=422, detail="Episode has no script to synthesize."
        )

    episode.audio_status = "unavailable"
    episode.audio_path = None
    warning = _sync_audio(episode)
    db.commit()
    db.refresh(episode)
    material = db.get(Material, episode.material_id)
    out = _episode_out(episode, material)
    out.warning = warning
    return out
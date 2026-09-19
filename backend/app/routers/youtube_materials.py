from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Material
from app.schemas import CreateYoutubeMaterial, MaterialOut
from app.services import transcript, youtube

router = APIRouter(prefix="/api/materials", tags=["youtube"])


def _to_out(m: Material) -> MaterialOut:
    return MaterialOut(
        id=m.id,
        title=m.title,
        content=m.content,
        source_type=m.source_type,
        source_url=m.source_url,
        char_count=len(m.content),
        word_count=len(m.content.split()),
        created_at=m.created_at,
    )


@router.post("/youtube", response_model=MaterialOut, status_code=201)
def create_youtube_material(
    payload: CreateYoutubeMaterial, db: Session = Depends(get_db)
):
    try:
        video_id = youtube.parse_youtube_url(payload.url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    try:
        content = transcript.fetch_transcript(video_id)
    except transcript.TranscriptError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    meta = youtube.fetch_video_metadata(video_id)
    title = (
        (payload.title or meta.get("title") or f"YouTube Video {video_id}").strip()
        or f"YouTube Video {video_id}"
    )[:255]

    material = Material(
        title=title,
        content=content,
        source_type="youtube",
        source_url=youtube.canonical_url(video_id),
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return _to_out(material)
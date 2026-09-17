from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Flashcard, Material
from app.schemas import CreateFlashcards, FlashcardOut
from app.services.ai import generate_flashcards as ai_generate_flashcards

router = APIRouter(prefix="/api/flashcards", tags=["flashcards"])


def _to_out(cards: list[Flashcard]) -> list[FlashcardOut]:
    return [FlashcardOut(id=c.id, front=c.front, back=c.back) for c in cards]


@router.get("", response_model=list[FlashcardOut])
def get_flashcards(
    material_id: int = Query(...), db: Session = Depends(get_db)
):
    cards = (
        db.query(Flashcard)
        .filter(Flashcard.material_id == material_id)
        .order_by(Flashcard.sort_order)
        .all()
    )
    return _to_out(cards)


@router.post("", response_model=list[FlashcardOut], status_code=201)
def create_flashcards(payload: CreateFlashcards, db: Session = Depends(get_db)):
    material = db.get(Material, payload.material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")

    db.query(Flashcard).filter(Flashcard.material_id == material.id).delete()
    db.flush()

    _, cards = ai_generate_flashcards(
        material.content,
        count=8,
        provider=payload.provider,
        model_name=payload.model_name,
    )

    saved = []
    for idx, card in enumerate(cards):
        fc = Flashcard(
            material_id=material.id,
            front=card["front"],
            back=card["back"],
            sort_order=idx,
            provider=payload.provider,
            model_name=payload.model_name,
        )
        db.add(fc)
        saved.append(fc)

    db.commit()
    for fc in saved:
        db.refresh(fc)
    return _to_out(saved)
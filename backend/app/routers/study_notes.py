from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Material, StudyNote
from app.schemas import (
    CreateStudyNotes,
    StudyNoteKeyConcept,
    StudyNoteSection,
    StudyNotesOut,
)
from app.services.ai import generate_study_notes as ai_generate_study_notes

router = APIRouter(prefix="/api/study-notes", tags=["study-notes"])


def _to_out(note: StudyNote) -> StudyNotesOut:
    return StudyNotesOut(
        id=note.id,
        material_id=note.material_id,
        title=note.title,
        summary=note.summary,
        sections=[StudyNoteSection(**s) for s in note.sections],
        key_concepts=[StudyNoteKeyConcept(**kc) for kc in note.key_concepts],
        generated_by=note.generated_by,
        provider=note.provider,
        model_name=note.model_name,
        created_at=note.created_at,
    )


@router.get("", response_model=StudyNotesOut | None)
def get_study_notes(
    material_id: int = Query(...), db: Session = Depends(get_db)
):
    note = (
        db.query(StudyNote)
        .filter(StudyNote.material_id == material_id)
        .order_by(StudyNote.id.desc())
        .first()
    )
    return _to_out(note) if note else None


@router.post("", response_model=StudyNotesOut, status_code=201)
def create_study_notes(payload: CreateStudyNotes, db: Session = Depends(get_db)):
    material = db.get(Material, payload.material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")

    db.query(StudyNote).filter(StudyNote.material_id == material.id).delete()
    db.flush()

    generated_by, notes, warning = ai_generate_study_notes(
        material.content,
        provider=payload.provider,
        model_name=payload.model_name,
    )

    note = StudyNote(
        material_id=material.id,
        title=notes["title"],
        summary=notes["summary"],
        sections=notes["sections"],
        key_concepts=notes["key_concepts"],
        generated_by=generated_by,
        provider=payload.provider,
        model_name=payload.model_name,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    out = _to_out(note)
    out.warning = warning or None
    return out
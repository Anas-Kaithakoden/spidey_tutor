from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Material
from app.schemas import CreateMaterial, MaterialOut
from app.services.pdf import extract_pdf_text

router = APIRouter(prefix="/api/materials", tags=["materials"])


def _to_out(m: Material) -> MaterialOut:
    return MaterialOut(
        id=m.id,
        title=m.title,
        content=m.content,
        source_type=m.source_type,
        char_count=len(m.content),
        word_count=len(m.content.split()),
        created_at=m.created_at,
    )


@router.post("", response_model=MaterialOut, status_code=201)
def create_material(payload: CreateMaterial, db: Session = Depends(get_db)):
    title = (payload.title or "Pasted Material").strip() or "Pasted Material"
    material = Material(
        title=title,
        content=payload.text.strip(),
        source_type="text",
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return _to_out(material)


@router.post("/pdf", response_model=MaterialOut, status_code=201)
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    data = file.file.read()

    try:
        content = extract_pdf_text(data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    title = file.filename.rsplit(".", 1)[0] or "Uploaded PDF"
    material = Material(title=title, content=content, source_type="pdf")
    db.add(material)
    db.commit()
    db.refresh(material)
    return _to_out(material)


@router.get("/{material_id}", response_model=MaterialOut)
def get_material(material_id: int, db: Session = Depends(get_db)):
    material = db.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")
    return _to_out(material)
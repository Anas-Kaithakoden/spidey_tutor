from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Material
from app.schemas import CreateMaterial, MaterialOut
from app.services.image import extract_image_text
from app.services.office import extract_office_text
from app.services.pdf import extract_pdf_text

router = APIRouter(prefix="/api/materials", tags=["materials"])


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


@router.post("/image", response_model=MaterialOut, status_code=201)
def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp")):
        raise HTTPException(status_code=400, detail="Only image files are supported (png, jpg, jpeg, webp, bmp).")

    data = file.file.read()
    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image too large (max 10 MB).")

    try:
        content = extract_image_text(data, file.filename)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    title = file.filename.rsplit(".", 1)[0] or "Uploaded Image"
    material = Material(title=title, content=content, source_type="image")
    db.add(material)
    db.commit()
    db.refresh(material)
    return _to_out(material)


@router.post("/office", response_model=MaterialOut, status_code=201)
def upload_office(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith(
        (".docx", ".pptx", ".xlsx", ".xls", ".txt", ".md", ".csv")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only office files are supported (.docx, .pptx, .xlsx, .txt, .csv, .md).",
        )

    data = file.file.read()
    if len(data) > 15 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large (max 15 MB).")

    try:
        content = extract_office_text(data, file.filename)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    # infer type for UI badge
    lower = file.filename.lower()
    if lower.endswith(".docx"):
        stype = "docx"
    elif lower.endswith(".pptx"):
        stype = "pptx"
    elif lower.endswith((".xlsx", ".xls")):
        stype = "xlsx"
    else:
        stype = "office"
    title = file.filename.rsplit(".", 1)[0] or "Uploaded Office Doc"
    material = Material(title=title, content=content, source_type=stype)
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
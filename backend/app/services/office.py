import io
import logging

logger = logging.getLogger(__name__)


def extract_office_text(data: bytes, filename: str) -> str:
    """Extract text from office documents: docx, pptx, xlsx, txt, odt."""
    lower = filename.lower()
    try:
        if lower.endswith(".docx"):
            return _extract_docx(data)
        if lower.endswith(".pptx"):
            return _extract_pptx(data)
        if lower.endswith(".xlsx") or lower.endswith(".xls"):
            return _extract_xlsx(data)
        if lower.endswith(".txt") or lower.endswith(".md") or lower.endswith(".csv"):
            return data.decode("utf-8", errors="ignore").strip()
        raise ValueError(
            f"Unsupported office format: {filename}. Supported: .docx, .pptx, .xlsx, .txt, .csv"
        )
    except ValueError:
        raise
    except Exception as exc:
        logger.exception("Office extraction failed (%s): %s", filename, exc)
        raise ValueError(f"Could not read office file: {exc}") from exc


def _extract_docx(data: bytes) -> str:
    try:
        import docx  # python-docx
    except ImportError as exc:
        raise ValueError("python-docx not installed. Run pip install python-docx") from exc

    doc = docx.Document(io.BytesIO(data))
    parts = []
    for para in doc.paragraphs:
        if para.text.strip():
            parts.append(para.text.strip())
    for table in doc.tables:
        for row in table.rows:
            row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
            if row_text:
                parts.append(row_text)
    text = "\n".join(parts).strip()
    if not text:
        raise ValueError("No extractable text found in this .docx file.")
    return text


def _extract_pptx(data: bytes) -> str:
    try:
        import pptx  # python-pptx
    except ImportError as exc:
        raise ValueError("python-pptx not installed. Run pip install python-pptx") from exc

    prs = pptx.Presentation(io.BytesIO(data))
    parts = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    t = para.text.strip()
                    if t:
                        parts.append(t)
            if shape.has_table:
                for row in shape.table.rows:
                    row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                    if row_text:
                        parts.append(row_text)
    text = "\n".join(parts).strip()
    if not text:
        raise ValueError("No extractable text found in this .pptx file.")
    return text


def _extract_xlsx(data: bytes) -> str:
    try:
        import openpyxl  # openpyxl
    except ImportError as exc:
        raise ValueError("openpyxl not installed. Run pip install openpyxl") from exc

    wb = openpyxl.load_workbook(io.BytesIO(data), data_only=True, read_only=True)
    parts = []
    for ws in wb.worksheets:
        parts.append(f"Sheet: {ws.title}")
        for row in ws.iter_rows(values_only=True):
            row_vals = [str(c).strip() for c in row if c is not None and str(c).strip()]
            if row_vals:
                parts.append(" | ".join(row_vals))
    text = "\n".join(parts).strip()
    if not text:
        raise ValueError("No extractable text found in this spreadsheet.")
    return text

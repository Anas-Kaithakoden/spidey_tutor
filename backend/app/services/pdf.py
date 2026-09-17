import logging

import pymupdf  # PyMuPDF

logger = logging.getLogger(__name__)


def extract_pdf_text(data: bytes) -> str:
    """Extract plain text from uploaded PDF bytes using PyMuPDF."""
    try:
        doc = pymupdf.open(stream=data, filetype="pdf")
    except Exception as exc:
        logger.warning("Could not open PDF: %s", exc)
        raise ValueError("Could not read this PDF file. It may be corrupted or password-protected.")

    pages = [page.get_text("text") for page in doc]
    doc.close()

    text = "\n".join(pages).strip()
    if not text:
        raise ValueError(
            "No extractable text found in this PDF. It may be a scanned/image-only document."
        )
    return text
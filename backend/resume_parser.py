import pdfplumber
import io
from fastapi import HTTPException


def extract_text_from_pdf(file_bytes: bytes, filename: str) -> str:
    """
    Extract plain text from a PDF file given as raw bytes.
    Raises HTTPException on failure.
    """
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text.strip())

            full_text = "\n\n".join(pages_text)

        if not full_text.strip():
            raise HTTPException(
                status_code=422,
                detail="No readable text found in the PDF. The file may be scanned or image-based.",
            )

        return full_text

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse PDF: {str(e)}",
        )
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")  # always finds .env next to main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import AnalyzeRequest, AnalyzeResponse, UploadResponse
from resume_parser import extract_text_from_pdf
from ai_engine import analyze_resume_with_ai

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AI Resume Analyzer API",
    description="Upload a resume and compare it to a job description using AI.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS Configuration (Fix for Vercel → Render communication)
# ---------------------------------------------------------------------------
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "https://ai-resume-analyzer-dun-one.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "message": "AI Resume Analyzer API is running."
    }

# ---------------------------------------------------------------------------
# POST /upload-resume
# Accepts a PDF, returns extracted text.
# ---------------------------------------------------------------------------
@app.post("/upload-resume", response_model=UploadResponse, tags=["Resume"])
async def upload_resume(file: UploadFile = File(...)):

    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Only PDFs are accepted."
        )

    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File too large. Maximum size is 10 MB."
        )

    extracted_text = extract_text_from_pdf(
        file_bytes,
        file.filename or "resume.pdf"
    )

    return UploadResponse(
        filename=file.filename or "resume.pdf",
        extracted_text=extracted_text,
        char_count=len(extracted_text)
    )

# ---------------------------------------------------------------------------
# POST /analyze
# Accepts JSON: { resume_text, job_description }
# ---------------------------------------------------------------------------
@app.post("/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
async def analyze(request: AnalyzeRequest):

    if not request.job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    if not request.resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty."
        )

    return analyze_resume_with_ai(
        request.resume_text,
        request.job_description
    )
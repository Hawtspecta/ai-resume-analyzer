from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import AnalyzeResponse, UploadResponse
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

# CORS — allows the React frontend running on localhost:5173 (Vite default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "AI Resume Analyzer API is running."}


# ---------------------------------------------------------------------------
# POST /upload-resume
# Accepts a PDF, returns extracted text.
# ---------------------------------------------------------------------------
@app.post("/upload-resume", response_model=UploadResponse, tags=["Resume"])
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a PDF resume and extract its text content.
    """
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Only PDFs are accepted.",
        )

    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(file_bytes) > 10 * 1024 * 1024:  # 10 MB limit
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10 MB.")

    extracted_text = extract_text_from_pdf(file_bytes, file.filename or "resume.pdf")

    return UploadResponse(
        filename=file.filename or "resume.pdf",
        extracted_text=extracted_text,
        char_count=len(extracted_text),
    )


# ---------------------------------------------------------------------------
# POST /analyze
# Accepts multipart form: file (PDF) + job_description (str)
# Matches exactly what the frontend sends in api.ts → analyzeResume()
# ---------------------------------------------------------------------------
@app.post("/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
async def analyze(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):
    """
    Analyze a resume PDF against a job description using AI.
    Returns skill match percentage, missing skills, suggestions, and a learning path.
    """
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10 MB.")

    # Step 1: Extract text from PDF
    resume_text = extract_text_from_pdf(file_bytes, file.filename or "resume.pdf")

    # Step 2: Send to AI for analysis
    result = analyze_resume_with_ai(resume_text, job_description)

    return result
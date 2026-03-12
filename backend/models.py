from pydantic import BaseModel
from typing import List


class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str


class AnalyzeResponse(BaseModel):
    skill_match: float
    missing_skills: List[str]
    suggestions: List[str]
    learning_path: List[str]


class UploadResponse(BaseModel):
    filename: str
    extracted_text: str
    char_count: int
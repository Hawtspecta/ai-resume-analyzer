from pydantic import BaseModel
from typing import List


class AnalyzeResponse(BaseModel):
    skill_match: float
    missing_skills: List[str]
    suggestions: List[str]
    learning_path: List[str]


class UploadResponse(BaseModel):
    filename: str
    extracted_text: str
    char_count: int
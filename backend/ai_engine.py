import os
import json
import requests
from fastapi import HTTPException
from models import AnalyzeResponse

# ---------------------------------------------------------------------------
# xAI / Grok API Configuration
# ---------------------------------------------------------------------------
# Set this environment variable before starting the server:
#   export XAI_API_KEY="your_key_here"
XAI_API_KEY: str = os.getenv("XAI_API_KEY", "")

# xAI uses an OpenAI-compatible REST endpoint
XAI_API_URL: str = "https://api.x.ai/v1/chat/completions"

# Latest stable Grok model — change to "grok-beta" if needed
XAI_MODEL: str = "grok-3-mini"


# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """\
You are a senior technical recruiter with 10+ years of experience evaluating \
software engineering resumes.

Compare the provided RESUME against the JOB DESCRIPTION and return a \
single JSON object — no markdown, no explanation, no extra text.

The JSON must contain exactly these four keys:

{
  "skill_match": <integer 0-100>,
  "missing_skills": [<string>, ...],
  "suggestions":    [<string>, ...],
  "learning_path":  [<string>, ...]
}

Definitions:
- skill_match     : Overall match percentage between resume and job requirements.
- missing_skills  : Skills/technologies in the job description absent from the resume (max 8).
- suggestions     : Specific, actionable resume improvements the candidate should make (max 5).
- learning_path   : Ordered list of topics or resources to close the skill gap (max 5).

Return ONLY the raw JSON object. Do not wrap it in code fences.\
"""


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def analyze_resume_with_ai(resume_text: str, job_description: str) -> AnalyzeResponse:
    """
    Send resume_text and job_description to the xAI Grok API.
    Returns a validated AnalyzeResponse containing:
      - skill_match (float 0-100)
      - missing_skills (list[str])
      - suggestions (list[str])
      - learning_path (list[str])
    """
    _check_api_key()
    raw_content = _call_xai_api(resume_text, job_description)
    parsed = _parse_json(raw_content)
    return _build_response(parsed)


# ---------------------------------------------------------------------------
# Step 1 — Guard: API key present?
# ---------------------------------------------------------------------------
def _check_api_key() -> None:
    if not XAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail=(
                "XAI_API_KEY environment variable is not set. "
                "Export it before starting the server:  export XAI_API_KEY=your_key"
            ),
        )


# ---------------------------------------------------------------------------
# Step 2 — HTTP call to xAI
# ---------------------------------------------------------------------------
def _call_xai_api(resume_text: str, job_description: str) -> str:
    """
    POST to https://api.x.ai/v1/chat/completions and return the raw
    assistant message string.
    """
    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": XAI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"RESUME:\n{resume_text}\n\n"
                    f"JOB DESCRIPTION:\n{job_description}"
                ),
            },
        ],
        "temperature": 0.2,   # Low temp = more deterministic, consistent JSON
        "max_tokens": 1024,
    }

    try:
        response = requests.post(
            XAI_API_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Request to xAI API timed out. Please try again.",
        )
    except requests.exceptions.HTTPError as exc:
        http_status = exc.response.status_code if exc.response is not None else 500
        try:
            api_message = exc.response.json().get("error", {}).get("message", str(exc))
        except Exception:
            api_message = str(exc)
        raise HTTPException(
            status_code=http_status,
            detail=f"xAI API error ({http_status}): {api_message}",
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to xAI API. Check your network or API URL.",
        )
    except requests.exceptions.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unexpected request failure: {str(exc)}",
        )

    # Pull out the assistant reply text
    try:
        return response.json()["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unexpected xAI response structure: {str(exc)}",
        )


# ---------------------------------------------------------------------------
# Step 3 — Parse JSON from the model's reply
# ---------------------------------------------------------------------------
def _parse_json(raw: str) -> dict:
    """
    Parse the model output as JSON.
    Defensively strips markdown code fences in case the model ignores instructions.
    """
    cleaned = raw

    # Handle ```json ... ``` or ``` ... ```
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        # Drop the opening fence line (```json or ```) and closing fence line
        start = 1
        end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        cleaned = "\n".join(lines[start:end]).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                f"xAI returned invalid JSON: {str(exc)}. "
                f"Raw (first 300 chars): {raw[:300]}"
            ),
        )

    if not isinstance(data, dict):
        raise HTTPException(
            status_code=502,
            detail=f"Expected a JSON object from xAI, got: {type(data).__name__}",
        )

    return data


# ---------------------------------------------------------------------------
# Step 4 — Coerce parsed dict → typed AnalyzeResponse
# ---------------------------------------------------------------------------
def _build_response(data: dict) -> AnalyzeResponse:
    try:
        skill_match = float(data.get("skill_match", 0))
        skill_match = max(0.0, min(100.0, skill_match))  # clamp to 0-100

        return AnalyzeResponse(
            skill_match=skill_match,
            missing_skills=[str(s) for s in data.get("missing_skills", [])],
            suggestions=[str(s) for s in data.get("suggestions", [])],
            learning_path=[str(s) for s in data.get("learning_path", [])],
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to build response from AI output: {str(exc)}",
        )
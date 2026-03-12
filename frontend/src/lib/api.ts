import axios from "axios";

const API_BASE = "http://localhost:8000";

export interface UploadResult {
  filename: string;
  extracted_text: string;
  char_count: number;
}

export interface AnalysisResult {
  skill_match: number;
  missing_skills: string[];
  suggestions: string[];
  learning_path: string[];
}

export async function uploadResume(file: File): Promise<UploadResult> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await axios.post(`${API_BASE}/upload-resume`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function analyzeResume(
  resume_text: string,
  job_description: string
): Promise<AnalysisResult> {
  const res = await axios.post(`${API_BASE}/analyze`, {
    resume_text,
    job_description,
  });
  return res.data;
}

// Mock for demo when backend is unavailable
export function getMockResult(): AnalysisResult {
  return {
    skill_match: 75,
    missing_skills: ["Docker", "AWS", "System Design"],
    suggestions: [
      "Add backend projects to showcase full-stack skills",
      "Mention GitHub contributions and open-source work",
      "Quantify achievements with metrics and numbers",
    ],
    learning_path: [
      "Learn Docker fundamentals and containerization",
      "Learn cloud basics with AWS or GCP",
      "Study system design patterns",
      "Practice with real-world projects",
    ],
  };
}

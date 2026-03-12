# 🚀 AI Resume Analyzer

An AI-powered web application that analyzes resumes, provides ATS-style feedback, identifies missing skills, and suggests improvements using modern AI models.

The application allows users to upload a resume and receive intelligent insights about how well their resume aligns with industry expectations.

---

# 🌐 Live Demo

Frontend:

```
https://ai-resume-analyzer-dun-one.vercel.app/
```

Backend API:

```
https://ai-resume-backend-aox1.onrender.com/docs
```

---

# 🧠 Features

• Upload and analyze resumes in PDF format
• AI-powered resume feedback and suggestions
• Missing skills detection
• ATS-style scoring and improvement tips
• Fast API responses using FastAPI backend
• Clean and responsive frontend interface

---

# 🏗️ Tech Stack

### Frontend

* React / TypeScript
* Modern UI components
* API integration

### Backend

* FastAPI
* Python
* PDF parsing with pdfplumber
* AI analysis via Groq API

### Deployment

* Frontend: Vercel
* Backend: Render

---

# 📂 Project Structure

```
ai-resume-analyzer
│
├── backend
│   ├── main.py
│   ├── ai_engine.py
│   ├── requirements.txt
│   └── .env
│
├── frontend
│   ├── src
│   ├── components
│   └── api.ts
│
├── runtime.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Local Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/hawtspecta/ai-resume-analyzer.git
cd ai-resume-analyzer
```

---

### 2️⃣ Backend Setup

```
cd backend
pip install -r requirements.txt
```

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

Run the server:

```
uvicorn main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

---

### 3️⃣ Frontend Setup

```
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 🔑 Environment Variables

Backend requires:

```
GROQ_API_KEY=your_groq_api_key
```

---

# 🧪 API Endpoint

### Analyze Resume

```
POST /analyze
```

Upload a PDF resume and receive AI feedback.

Example response:

```json
{
  "score": 82,
  "missing_skills": [
    "Docker",
    "System Design"
  ],
  "suggestions": [
    "Add quantified achievements",
    "Highlight backend experience"
  ]
}
```

---

# 📈 Future Improvements

• Resume rewriting suggestions
• Job description matching
• Skill gap analysis
• AI generated improved bullet points
• Resume keyword optimization

---

# 👨‍💻 Author

Sahana Nayak

GitHub:
[https://github.com/Hawtspecta](https://github.com/Hawtspecta)

---

# ⭐ Contributing

Contributions and suggestions are welcome!
Feel free to fork the repository and submit pull requests.


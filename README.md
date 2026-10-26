# Career AI — AI-Powered Career Development Platform

> **College Minor Project MVP**  
> An intelligent, end-to-end career readiness suite featuring automated Resume Analysis, ATS Compatibility Matching, AI-Assisted Resume Enhancement, Interactive Mock Interviews, Skill Gap Identification, and Phased Career Roadmaps.

---

## 📌 Project Overview
In modern recruitment ecosystems, candidates face stringent automated Applicant Tracking Systems (ATS) and demanding multi-stage technical/behavioral interviews. Many job seekers lack objective feedback on how well their resumes match industry expectations and how their current skill sets compare to real-world job roles.

**Career AI** addresses this challenge by providing a unified, privacy-first career acceleration platform. Built with Python, Streamlit, and local AI capabilities (Ollama with robust deterministic fallback engines), the application operates without mandatory external paid APIs, ensuring total privacy, zero recurring cloud costs, and high performance during academic demonstrations and production deployments.

---

## 🚀 Key Features & Modules

### 1. 📊 Executive Dashboard (`app.py`)
- Real-time diagnostics for AI connection (Ollama status vs. offline deterministic fallback).
- Global candidate profile management across sessions.
- Platform telemetry metrics (Resumes evaluated, ATS checks run, Mock interviews logged).
- Recent activity feed connected live to SQLite storage.

### 2. 📄 Resume Analyzer (`pages/1_Resume_Analyzer.py`)
- **PDF Extraction:** Direct in-memory parsing using PyMuPDF (`pymupdf`).
- **Section Audit:** Rule-based detection of core sections (Contact Details, Summary, Experience, Education, Skills, Projects, Certifications).
- **Skill Extraction:** Zero-hallucination taxonomy engine scanning 250+ categorized programming languages, frameworks, databases, cloud tools, and soft skills.
- **Multi-Factor Scoring (0–100):** Visualized via Plotly gauge charts, auditing contact richness, completeness, action verbs, and quantifiable metrics.

### 3. 🎯 ATS Checker (`pages/2_ATS_Checker.py`)
- **Dual Natural Language Processing Engine:** Combines TF-IDF unigram vectorization with Cosine Similarity and exact target keyword extraction.
- **Gap Analysis:** Visual comparison of matched vs. missing skills and tools.
- **Explainable Ranking:** Transparent score explanation demystifying why a candidate received their score, along with guidance to avoid keyword stuffing.

### 4. ✍️ AI Resume Improver (`pages/3_AI_Resume_Improver.py`)
- **Ollama Integration:** Sends prompts to local LLMs (e.g., Llama 3, Mistral, Phi-3).
- **Deterministic Fallback Engine:** Employs rule-based transformations replacing passive phrasing with executive action verbs (e.g., *"worked on"* → *"Architected & Deployed"*).
- **Integrity Guarantee:** Never invents unearned achievements, degrees, or false metrics; prompts the user to insert quantifiable outcomes.

### 5. 🎙️ AI Mock Interview Simulation (`pages/4_Mock_Interview.py`)
- **Role & Category Selection:** Technical and HR/Behavioral tracks for Software Engineers, Data Scientists, DevOps, and Frontend Developers.
- **STAR Methodology Scoring:** Evaluates answers for Situation, Task, Action, and measurable Results.
- **Performance Analytics:** Historical performance tracking with Plotly trend line visualization and persistent SQLite session logging.

### 6. 🔍 Skill Gap Analyzer (`pages/5_Skill_Gap.py`)
- **Role Benchmarking:** Evaluates current skills against curated industry standards.
- **Priority Tiering:** Distinguishes between **High Priority** (core requirements), **Medium Priority** (stack tools), and **Low Priority** (bonus differentiators).
- **Strategic Action Plan:** Clear recommendations on what to learn first.

### 7. 🗺️ Career Roadmap Generator (`pages/6_Career_Roadmap.py`)
- **3-Phase Milestones:** Beginner (Foundations), Intermediate (Frameworks & Systems), and Advanced (Production, Cloud & Scale).
- **Curated Projects & Resources:** Hands-on portfolio project recommendations and direct learning links.

### 8. 📈 Comprehensive Career Report (`pages/7_Career_Report.py`)
- **Composite Employability Index:** Aggregates scores across Resume, ATS, Interview, and Skill Readiness.
- **Multi-Axis Radar Chart:** Visualizes multi-dimensional candidate readiness.
- **Export Formats:** One-click downloads for Markdown (`.md`) and styled printable HTML (`.html`).

---

## 🏗️ System Architecture

```
Career AI Architecture
│
├── Frontend / Presentation Layer
│   └── Streamlit Multi-Page Framework with Responsive Theming & Plotly Charts
│
├── Core Analytics & Processing Engine
│   ├── resume_analyzer.py  --> PyMuPDF text parser, section & skill taxonomy auditor
│   ├── ats_engine.py       --> TF-IDF Vectorizer & Cosine Similarity match engine
│   ├── ai_service.py       --> Ollama REST client + Deterministic Fallback Rules
│   └── career_engine.py    --> Benchmark comparisons, skill gap calculator & report compiler
│
├── Persistence Layer
│   └── SQLite Database (data/career_ai.db)
│       ├── resumes
│       ├── ats_analyses
│       ├── interview_sessions
│       ├── skill_gap_records
│       └── career_reports
│
└── Local AI Inference Layer (Optional)
    └── Ollama (http://localhost:11434) with local models (llama3, mistral, phi3)
```

---

## 💻 Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Framework** | Streamlit 1.65+ | Modern, interactive web UI |
| **Language** | Python 3.10+ | Core application logic |
| **PDF Processing** | PyMuPDF (`pymupdf`) | High-fidelity resume text extraction |
| **NLP & ML** | Scikit-Learn | TF-IDF vectorization & Cosine Similarity |
| **Data & Math** | Pandas, NumPy | Data structures and matrix computations |
| **Visualizations**| Plotly | Interactive gauge, radar, pie, and bar charts |
| **Database** | SQLite 3 | Self-contained persistent database |
| **Local AI** | Ollama API / HTTP | Optional private local LLM inference |

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher installed
- Git installed (optional)

### 2. Clone / Open Workspace
Navigate to the project root directory:
```bash
cd "c:\Users\nisha\OneDrive\Desktop\minor project"
```

### 3. Install Dependencies
Install all required libraries via pip:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Application

Start the Streamlit application with:
```bash
streamlit run app.py
```

Once started, open your web browser and navigate to:
```
http://localhost:8501
```

---

## 🦙 Ollama / Local AI Setup (Optional)

Career AI works out-of-the-box without Ollama by automatically engaging its **high-accuracy deterministic fallback engine**. 

To connect local AI models:
1. Download and install Ollama from [ollama.com](https://ollama.com).
2. Pull a model in your terminal:
   ```bash
   ollama pull llama3
   # OR
   ollama pull mistral
   # OR
   ollama pull phi3
   ```
3. Start the Ollama server:
   ```bash
   ollama serve
   ```
4. Refresh the Career AI dashboard. The system indicator in the sidebar and dashboard will automatically turn green (**Ollama Connected**).

---

## 🗄️ Database Information

All data is automatically managed using SQLite in `data/career_ai.db`. The database is automatically initialized on the first application launch.

### Tables:
1. `resumes`: Stores extracted text, detected sections, skills, quality scores, and recommendations.
2. `ats_analyses`: Stores target job titles, match scores, cosine similarity, keyword density, and matched/missing keyword arrays.
3. `interview_sessions`: Stores role, category, question-answer pairs, scores, and STAR evaluations.
4. `skill_gap_records`: Stores role benchmarks, acquired skills, and prioritized gap mappings.
5. `career_reports`: Stores aggregated employability reports and summaries.

---

## ⚠️ Project Limitations
- **PDF Layouts:** Non-standard multi-column or graphic-heavy image resumes (scanned images without OCR) may require text preprocessing.
- **Local Compute:** Inference speed for Ollama LLM mode depends on local hardware (GPU/RAM).
- **Static Benchmarks:** Fallback role benchmarks represent current market medians and may vary by niche industry.

---

## 🔮 Future Enhancements
- Integration of Tesseract OCR for scanned PDF and image resumes.
- Voice-to-Text (STT) and Text-to-Speech (TTS) for conversational voice-based mock interviews.
- LinkedIn profile scraping and GitHub repository portfolio analysis.
- Multi-user authentication and role-based permissions (Student vs. Career Counselor).

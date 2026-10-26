# ACADEMIC MINOR PROJECT REPORT

## PROJECT TITLE:
**AI-Powered Career Development Platform with Resume Analysis and Mock Interviews**  
*(Application Name: Career AI)*

---

## 1. ABSTRACT
In today's highly competitive tech job market, job seekers encounter significant hurdles in transitioning from academic preparation to corporate employment. Traditional recruitment procedures rely heavily on automated Applicant Tracking Systems (ATS) to filter out resumes before human recruiters ever inspect them. Furthermore, candidates frequently struggle with identifying specific skill deficiencies and lack realistic technical and behavioral interview practice.

This project proposes **Career AI**, a comprehensive, privacy-first career development platform engineered using Python, Streamlit, Scikit-Learn, PyMuPDF, SQLite, and local Artificial Intelligence (Ollama with robust deterministic fallback engines). The application provides automated PDF resume parsing, section audits, taxonomy-based skill extraction, TF-IDF cosine-similarity ATS compatibility matching, STAR-methodology mock interviews, role-based skill gap identification, milestone career roadmaps, and unified employability reporting. Operating entirely on local compute without mandatory paid API subscriptions, Career AI delivers a robust, accessible, and high-impact solution for student career advancement.

---

## 2. PROBLEM STATEMENT
Current students and early-career job applicants face three critical disadvantages:
1. **Opaque ATS Screening:** Over 75% of resumes are eliminated by ATS software due to formatting flaws, missing keywords, or poor semantic relevance, with zero actionable feedback provided to the applicant.
2. **Ambiguous Skill Requirements:** Students struggle to accurately evaluate their technical readiness against industry job descriptions, resulting in unfocused learning efforts.
3. **Lack of Accessible Interview Preparation:** High-quality mock interview coaching is often cost-prohibitive, while commercial AI tools require cloud API fees and expose personal resume data to third-party providers.

There is a clear need for an integrated, local, private, and cost-free platform that audits resumes, simulates interviews, evaluates skill gaps, and generates structured career roadmaps.

---

## 3. OBJECTIVES
The principal objectives of Career AI are:
- To implement in-memory PDF parsing and structural auditing to evaluate resume quality without data loss.
- To formulate an ATS matching engine leveraging Natural Language Processing (TF-IDF vectorization and Cosine Similarity) to benchmark resumes against job descriptions.
- To establish a non-fabricating AI resume improvement module that transforms passive descriptions into impact-oriented bullet points.
- To design an interactive Mock Interview simulation that scores technical and behavioral responses against the STAR (Situation, Task, Action, Result) methodology.
- To develop a multi-tiered Skill Gap Analyzer calculating a candidate's readiness score against standard industry roles.
- To generate progressive, phased engineering roadmaps (Beginner → Intermediate → Advanced).
- To aggregate all metrics into an executive Career Readiness Report with downloadable Markdown and HTML exports.
- To build a fully offline-capable architecture with deterministic fallback logic ensuring zero failure when local LLMs are absent.

---

## 4. EXISTING SYSTEM
Existing career assistance tools generally suffer from several limitations:
- **Commercial SaaS Tools (e.g., Jobscan, Resume Worded):** Require recurring paid subscriptions, limit monthly scans, and process user resumes on external cloud servers, raising data privacy concerns.
- **Generic AI Chatbots (e.g., ChatGPT web interface):** Require manual prompt engineering, frequently fabricate ("hallucinate") employment history or metrics, and lack structured database tracking.
- **Disjointed Solutions:** Candidates must use one tool for resume formatting, another for keyword checking, and a separate service for mock interviews, resulting in a fragmented experience.

---

## 5. PROPOSED SYSTEM
The proposed system, **Career AI**, unites all career preparation facets into a unified dashboard:
- **Single Cohesive Platform:** Manages the entire pipeline from resume parsing to interview readiness and learning roadmaps.
- **Local & Privacy-Preserving:** Operates on the user's workstation using SQLite and local LLMs (Ollama) or intelligent heuristic fallback engines.
- **No Paid API Dependency:** Ensures academic reproducibility and zero financial barrier for students.
- **Fact-Preserving AI:** Employs guardrails ensuring that AI suggestions strengthen phrasing and highlight missing metrics without inventing false accomplishments.
- **Persistent Progress Tracking:** Automatically records evaluations in a local SQLite database for historical trend analysis.

---

## 6. METHODOLOGY

### 6.1 Resume Parsing & Quality Auditing
Resumes are ingested as PDF byte streams and parsed using PyMuPDF (`pymupdf`). The text is analyzed using regular expressions and a comprehensive taxonomy of over 250 technical and soft skills. A quality scoring model evaluates five dimensions:
$$\text{Quality Score} = S_{\text{contact}} + S_{\text{sections}} + S_{\text{metrics}} + S_{\text{length}} + S_{\text{skills}}$$
where each category is weighted based on standard recruiting conventions.

### 6.2 ATS Compatibility Matching
Job descriptions and resume texts are cleaned and converted into vector representations using Scikit-Learn's `TfidfVectorizer` (with English stop-word removal and sublinear term frequency scaling). The semantic alignment is computed via Cosine Similarity:
$$\text{Cosine Similarity} = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$
In parallel, target keywords are extracted from the job description and compared against the resume. The composite ATS score is calculated as:
$$\text{ATS Score} = (0.60 \times \text{Keyword Match \%}) + (0.40 \times \text{Scaled Cosine Similarity})$$

### 6.3 Interview Evaluation & STAR Heuristics
Mock interview answers are assessed across four dimensions:
1. **Length & Depth:** Ensuring answers avoid brief one-liners while remaining concise (25–250 words).
2. **STAR Methodology:** Identifying markers for Situation, Task, Action, and measurable Results (e.g., percentage improvements, performance boosts).
3. **Role-Specific Vocabulary:** Checking technical terminology relevant to the selected domain.
4. **Tone & Decisiveness:** Flagging hesitant hedging phrases.

---

## 7. SYSTEM ARCHITECTURE

```
+-------------------------------------------------------------+
|                     Streamlit User Interface                |
|  (Dashboard, 7 Dedicated Multi-Page Modules, Plotly Charts) |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                      Business Logic Layer                   |
|  +--------------------+  +-------------------------------+  |
|  | resume_analyzer.py |  |        ats_engine.py          |  |
|  | (PyMuPDF, Regex)   |  | (TF-IDF, Cosine Similarity)   |  |
|  +--------------------+  +-------------------------------+  |
|  +--------------------+  +-------------------------------+  |
|  |    ai_service.py   |  |       career_engine.py        |  |
|  | (Ollama + Rules)   |  | (Benchmarks & Aggregation)    |  |
|  +--------------------+  +-------------------------------+  |
+-------------------------------------------------------------+
         |                                           |
         v                                           v
+-----------------------+                 +---------------------+
| Local SQLite Database |                 | Optional Local LLM  |
|  (data/career_ai.db)  |                 | (Ollama REST API)   |
+-----------------------+                 +---------------------+
```

---

## 8. APPLICATION MODULES

1. **Executive Dashboard (`app.py`):** System status, global session profile, KPI metrics, navigation cards, and recent activity feed.
2. **Resume Analyzer (`pages/1_Resume_Analyzer.py`):** In-memory PDF text extraction, section checklist, categorized skill tagging, and quality scoring gauge.
3. **ATS Checker (`pages/2_ATS_Checker.py`):** Resume vs. Job Description matching with keyword gap analysis and explainable scoring.
4. **AI Resume Improver (`pages/3_AI_Resume_Improver.py`):** Action-verb refactoring, grammar cleanup, and executive summary polishing.
5. **AI Mock Interview (`pages/4_Mock_Interview.py`):** Role-based technical/HR simulation, STAR answer feedback, and historical performance tracking.
6. **Skill Gap Analyzer (`pages/5_Skill_Gap.py`):** Role benchmarking, acquired vs. missing categorization (High, Medium, Low priority), and learning order guidance.
7. **Career Roadmap (`pages/6_Career_Roadmap.py`):** 3-stage progression plan detailing required competencies, practical portfolio projects, and learning references.
8. **Master Career Report (`pages/7_Career_Report.py`):** Consolidated Employability Index, 4-axis radar chart, and downloadable Markdown/HTML reports.

---

## 9. TECHNOLOGIES USED

- **Frontend & App Framework:** Streamlit (v1.65+)
- **Core Language:** Python (v3.10+)
- **Document Processing:** PyMuPDF (`pymupdf` v1.28+)
- **Machine Learning & NLP:** Scikit-Learn (`scikit-learn` v1.9+)
- **Data Manipulation:** Pandas (v2.3+), NumPy (v2.5+)
- **Interactive Visualization:** Plotly (v7.1+)
- **Database:** SQLite 3
- **Local AI:** Ollama (via HTTP REST interface)

---

## 10. EXPECTED RESULTS & PERFORMANCE
- **Resume Parsing:** Accurately extracts raw text and identifies standard sections within 100 milliseconds for standard PDF resumes.
- **ATS Matching:** Accurately captures both exact keyword matches and high-level semantic alignment, preventing false positives from keyword stuffing.
- **Deterministic Reliability:** In environments without Ollama, 100% of the platform's features function smoothly through intelligent rule-based algorithms.
- **Zero Hallucination:** Academic and factual integrity is preserved across all resume enhancement and analysis tasks.

---

## 11. LIMITATIONS
- Text extraction relies on digital text layers in PDFs; image-only scanned documents without embedded text require an optical character recognition (OCR) preprocessor.
- Deterministic roadmaps represent predefined industry standards and cannot dynamically adapt to obscure non-standard tech stacks without an active LLM.

---

## 12. FUTURE SCOPE
- **OCR Integration:** Adding Tesseract OCR support to ingest scanned resumes and image files.
- **Speech Interaction:** Integrating Whisper (Speech-to-Text) and Edge-TTS for realistic, conversational voice mock interviews.
- **Live Job Scraping:** Fetching live job postings from platforms like LinkedIn or Indeed to benchmark against current postings in real time.
- **Authentication:** Introducing role-based login systems for university placement cells and career mentors.

---

## 13. CONCLUSION
**Career AI** successfully fulfills the requirements of a complete, production-ready college minor project. By integrating natural language processing, vector similarity matching, interactive visualization, and local artificial intelligence, the application bridges the gap between academic education and industry hiring standards. Its local architecture guarantees total data privacy, eliminates cloud costs, and provides candidates with actionable insights to accelerate their career development.

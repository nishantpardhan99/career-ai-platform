"""
Resume Analyzer module for Career AI.
Extracts text from PDF resumes using PyMuPDF, detects sections, extracts skills,
computes a multi-factor quality score, and provides actionable recommendations.
"""

import re
from typing import Dict, Any, List, Tuple
try:
    import pymupdf
except ImportError:
    pymupdf = None

# Comprehensive skill taxonomy across categories
SKILL_TAXONOMY = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "c", "javascript", "typescript", "ruby", "php",
        "go", "golang", "rust", "kotlin", "swift", "dart", "r", "scala", "shell", "bash", "sql"
    ],
    "Frameworks & Libraries": [
        "react", "react.js", "angular", "vue", "vue.js", "next.js", "node.js", "express", "express.js",
        "django", "flask", "fastapi", "spring", "spring boot", "asp.net", "laravel",
        "pytorch", "tensorflow", "keras", "scikit-learn", "pandas", "numpy", "opencv",
        "tailwind", "bootstrap", "graphql", "jquery"
    ],
    "Databases & Storage": [
        "postgresql", "mysql", "sqlite", "mongodb", "redis", "cassandra", "oracle",
        "firebase", "elasticsearch", "neo4j", "dynamodb", "mariadb"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "google cloud", "gcp", "docker", "kubernetes",
        "terraform", "ansible", "jenkins", "github actions", "gitlab ci", "linux", "nginx", "ci/cd"
    ],
    "Developer Tools & Platforms": [
        "git", "github", "gitlab", "bitbucket", "jira", "postman", "figma", "vs code",
        "docker desktop", "webpack", "vite", "npm", "yarn"
    ],
    "Core Concepts & Practices": [
        "data structures", "algorithms", "rest api", "microservices", "object-oriented programming",
        "oop", "system design", "agile", "scrum", "unit testing", "tdd", "ci/cd", "machine learning",
        "deep learning", "nlp", "computer vision", "artificial intelligence"
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork", "collaboration", "problem solving",
        "critical thinking", "time management", "adaptability", "mentorship", "presentation"
    ]
}

# Standard resume section patterns
SECTION_PATTERNS = {
    "Contact Info": [r"\b(email|phone|mobile|linkedin|github|portfolio|address|contact)\b"],
    "Professional Summary": [r"\b(summary|objective|profile|about me|career objective|professional overview)\b"],
    "Education": [r"\b(education|academic background|qualifications|degrees|academics)\b"],
    "Work Experience": [r"\b(experience|work experience|employment|internships|work history|professional experience)\b"],
    "Skills": [r"\b(skills|technical skills|competencies|technologies|technical expertise|tech stack)\b"],
    "Projects": [r"\b(projects|academic projects|key projects|personal projects|portfolio projects)\b"],
    "Certifications": [r"\b(certifications|certificates|licenses|credentials|accreditations)\b"],
    "Achievements & Awards": [r"\b(achievements|awards|honors|publications|extracurricular|activities)\b"]
}

# Action verbs commonly looked for in strong resumes
STRONG_ACTION_VERBS = [
    "accelerated", "achieved", "analyzed", "architected", "automated", "built",
    "collaborated", "constructed", "created", "decreased", "delivered", "deployed",
    "designed", "developed", "engineered", "established", "executed", "expanded",
    "facilitated", "formulated", "generated", "implemented", "improved", "increased",
    "initiated", "instituted", "integrated", "launched", "led", "managed", "maximized",
    "minimized", "modeled", "monitored", "negotiated", "optimized", "orchestrated",
    "overhauled", "pioneered", "planned", "produced", "programmed", "reduced",
    "refactored", "resolved", "restructured", "revamped", "saved", "scaled",
    "spearheaded", "standardized", "streamlined", "strengthened", "transformed"
]


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text cleanly from a PDF byte stream using PyMuPDF (fitz).
    """
    if not pymupdf:
        raise ImportError("PyMuPDF is not installed. Please run `pip install pymupdf`.")

    doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    extracted_text = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        extracted_text.append(page.get_text("text"))
    doc.close()

    full_text = "\n".join(extracted_text)
    # Clean excessive whitespace while keeping structure
    full_text = re.sub(r"\r\n", "\n", full_text)
    return full_text.strip()


def detect_contact_info(text: str) -> Dict[str, Any]:
    """Detects presence of contact details (email, phone, LinkedIn, GitHub)."""
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    phone_pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    linkedin_pattern = r"(linkedin\.com/in/[a-zA-Z0-9_-]+|linkedin)"
    github_pattern = r"(github\.com/[a-zA-Z0-9_-]+|github)"

    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)
    linkedin = re.search(linkedin_pattern, text, re.IGNORECASE)
    github = re.search(github_pattern, text, re.IGNORECASE)

    return {
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "has_linkedin": bool(linkedin),
        "has_github": bool(github)
    }


def detect_sections(text: str) -> Dict[str, bool]:
    """
    Scans the text for headers identifying core resume sections.
    """
    detected = {}
    lines = text.split("\n")
    cleaned_lines = [line.strip().lower() for line in lines if line.strip()]

    for section_name, patterns in SECTION_PATTERNS.items():
        found = False
        for pattern in patterns:
            # Check individual lines for section header match
            for line in cleaned_lines:
                # Match line that looks like a header (e.g. length < 35 words/chars)
                if len(line) <= 40 and re.search(pattern, line):
                    found = True
                    break
            if found:
                break
        detected[section_name] = found

    return detected


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extracts recognized skills categorized by domain.
    Uses regex boundary matching to avoid substring false positives.
    """
    text_lower = " " + text.lower() + " "
    matched_categorized: Dict[str, List[str]] = {}

    for category, skill_list in SKILL_TAXONOMY.items():
        found_in_category = []
        for skill in skill_list:
            # Handle special symbols like C++, C#, .NET
            escaped_skill = re.escape(skill)
            if skill in ["c", "r"]:
                # Single letter needs strict non-alphanumeric boundary
                pattern = rf"(?<![a-zA-Z0-9_]){escaped_skill}(?![a-zA-Z0-9_])"
            else:
                pattern = rf"\b{escaped_skill}\b"

            if re.search(pattern, text_lower):
                found_in_category.append(skill.title() if len(skill) > 3 else skill.upper())

        if found_in_category:
            matched_categorized[category] = sorted(list(set(found_in_category)))

    return matched_categorized


def calculate_quality_score(text: str, sections: Dict[str, bool],
                            contact_info: Dict[str, Any],
                            skills_by_cat: Dict[str, List[str]]) -> Tuple[float, Dict[str, float], List[str]]:
    """
    Computes a comprehensive resume quality score (0-100) and actionable improvement suggestions.
    Score Breakdown:
    - Contact Details: 15 pts
    - Section Completeness: 35 pts
    - Action Verbs & Metrics: 20 pts
    - Length & Readability: 15 pts
    - Skill Depth: 15 pts
    """
    score_breakdown = {}
    suggestions = []

    # 1. Contact Information (15 pts)
    contact_score = 0.0
    if contact_info.get("email"):
        contact_score += 5.0
    else:
        suggestions.append("Missing contact email: Add a professional email address at the top of your resume.")

    if contact_info.get("phone"):
        contact_score += 4.0
    else:
        suggestions.append("Missing phone number: Ensure a valid mobile contact is visible.")

    if contact_info.get("has_linkedin"):
        contact_score += 3.0
    else:
        suggestions.append("Add a LinkedIn profile link to increase recruiter credibility.")

    if contact_info.get("has_github"):
        contact_score += 3.0
    else:
        suggestions.append("Add a GitHub or portfolio link to showcase verified code and technical projects.")

    score_breakdown["Contact Details"] = contact_score

    # 2. Section Completeness (35 pts)
    core_sections = {
        "Education": 8.0,
        "Work Experience": 10.0,
        "Skills": 8.0,
        "Projects": 6.0,
        "Professional Summary": 3.0
    }
    sec_score = 0.0
    for sec, pts in core_sections.items():
        if sections.get(sec, False):
            sec_score += pts
        else:
            if sec in ["Education", "Work Experience", "Skills"]:
                suggestions.append(f"Crucial section missing: Add a dedicated '{sec}' section.")
            else:
                suggestions.append(f"Recommended section missing: Consider adding a '{sec}' section.")

    score_breakdown["Section Completeness"] = sec_score

    # 3. Action Verbs & Quantifiable Metrics (20 pts)
    text_lower = text.lower()
    words = text_lower.split()
    verb_count = sum(1 for verb in STRONG_ACTION_VERBS if re.search(rf"\b{verb}\b", text_lower))
    # Detect metrics like percentages, numbers with +, dollars, etc.
    metrics_count = len(re.findall(r"\b\d+(?:%|\+|\$|x|k|m)?\b", text_lower))

    verb_pts = min(10.0, (verb_count / 8.0) * 10.0)
    metric_pts = min(10.0, (metrics_count / 6.0) * 10.0)
    score_breakdown["Impact & Metrics"] = round(verb_pts + metric_pts, 1)

    if verb_count < 5:
        suggestions.append("Use more executive action verbs (e.g., 'Spearheaded', 'Optimized', 'Architected') to begin bullet points.")
    if metrics_count < 4:
        suggestions.append("Quantify your accomplishments! Add measurable outcomes (e.g., 'boosted performance by 25%', 'handled 5,000+ requests').")

    # 4. Length & Readability (15 pts)
    total_words = len(words)
    readability_score = 0.0
    if 350 <= total_words <= 900:
        readability_score = 15.0
    elif 200 <= total_words < 350:
        readability_score = 10.0
        suggestions.append("Resume is somewhat brief (under 350 words). Expand upon project outcomes, methodologies, and duties.")
    elif total_words > 1200:
        readability_score = 9.0
        suggestions.append("Resume exceeds standard 1-2 page density (over 1200 words). Trim verbose descriptions to improve scannability.")
    else:
        readability_score = 6.0
        suggestions.append("Word count is suboptimal. Ensure adequate coverage of skills, coursework, and practical experience.")
    score_breakdown["Length & Structure"] = readability_score

    # 5. Skill Depth (15 pts)
    total_skills = sum(len(skills) for skills in skills_by_cat.values())
    skill_score = min(15.0, (total_skills / 10.0) * 15.0)
    score_breakdown["Skill Diversity"] = round(skill_score, 1)

    if total_skills < 6:
        suggestions.append("Limited technical/domain skills identified. Include more tools, languages, and frameworks in your skills section.")

    total_score = sum(score_breakdown.values())
    total_score = max(10.0, min(100.0, round(total_score, 1)))

    if not suggestions:
        suggestions.append("Excellent resume structure! Continue keeping skills updated with your latest accomplishments.")

    return total_score, score_breakdown, suggestions


def analyze_resume_text(text: str, filename: str = "Uploaded_Resume.pdf") -> Dict[str, Any]:
    """
    Main entry point to perform complete resume analysis on text.
    """
    contact_info = detect_contact_info(text)
    sections = detect_sections(text)
    skills_by_category = extract_skills(text)
    flat_skills = []
    for cat, items in skills_by_category.items():
        flat_skills.extend(items)
    flat_skills = sorted(list(set(flat_skills)))

    total_score, score_breakdown, suggestions = calculate_quality_score(
        text, sections, contact_info, skills_by_category
    )

    word_count = len(text.split())

    return {
        "filename": filename,
        "raw_text": text,
        "word_count": word_count,
        "contact_info": contact_info,
        "sections": sections,
        "skills_by_category": skills_by_category,
        "skills": flat_skills,
        "quality_score": total_score,
        "score_breakdown": score_breakdown,
        "suggestions": suggestions
    }

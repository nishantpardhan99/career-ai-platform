"""
ATS (Applicant Tracking System) Engine for Career AI.
Evaluates resume against a target job description using TF-IDF vectorization,
cosine similarity, keyword extraction, and gap analysis.
"""

import re
from typing import Dict, Any, List, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_analyzer import SKILL_TAXONOMY

# Curated multi-word industry phrases
VALID_PHRASES = {
    "data structures", "machine learning", "deep learning", "rest api", "restful api",
    "unit testing", "ci cd", "ci/cd", "microservices architecture", "system design",
    "cloud computing", "object oriented", "front end", "back end", "full stack",
    "version control", "agile scrum", "test driven development", "software development",
    "spring boot", "react js", "node js", "vue js", "next js", "express js"
}


def clean_text_for_nlp(text: str) -> str:
    """Cleans punctuation, lowercases, and normalizes text."""
    t = text.lower()
    # Normalize slashes in ci/cd
    t = t.replace("ci/cd", "cicd").replace("c++", "cpp").replace("c#", "csharp")
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def extract_key_phrases_from_job(job_text: str, top_k: int = 25) -> List[str]:
    """
    Extracts high-value technical keywords, technologies, and domain concepts
    from the target job description.
    """
    job_lower = " " + job_text.lower() + " "
    identified_keywords: Set[str] = set()

    # 1. Match against known skill taxonomy
    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            pattern = rf"\b{re.escape(skill)}\b"
            if re.search(pattern, job_lower):
                identified_keywords.add(skill.title() if len(skill) > 3 else skill.upper())

    # 2. Match standard multi-word engineering phrases
    for phrase in VALID_PHRASES:
        if phrase in job_lower:
            identified_keywords.add(phrase.title())

    # 3. TF-IDF unigram extraction for domain-specific terminology
    try:
        clean_job = clean_text_for_nlp(job_text)
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 1),
            stop_words='english',
            max_features=40
        )
        tfidf_matrix = vectorizer.fit_transform([clean_job])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        sorted_indices = scores.argsort()[::-1]

        for idx in sorted_indices:
            word = feature_names[idx]
            # Ignore common non-technical filler words
            if len(word) >= 3 and word not in {
                "years", "experience", "role", "looking", "candidate", "responsibilities",
                "requirements", "opportunity", "strong", "team", "working", "knowledge",
                "qualifications", "preferred", "ability", "needed", "plus", "must"
            }:
                # Re-map cpp / csharp / cicd
                display_word = "C++" if word == "cpp" else ("C#" if word == "csharp" else ("CI/CD" if word == "cicd" else word.title()))
                identified_keywords.add(display_word)
            if len(identified_keywords) >= top_k:
                break
    except Exception:
        pass

    return sorted(list(identified_keywords))[:top_k]


def calculate_ats_match(resume_text: str, job_text: str, job_title: str = "Target Role") -> Dict[str, Any]:
    """
    Calculates TF-IDF Cosine Similarity and Keyword Match Percentage
    between Resume and Job Description.
    """
    cleaned_resume = clean_text_for_nlp(resume_text)
    cleaned_job = clean_text_for_nlp(job_text)

    if not cleaned_resume or not cleaned_job:
        return {
            "match_score": 0.0,
            "cosine_similarity": 0.0,
            "keyword_match_pct": 0.0,
            "total_keywords_analyzed": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "recommendations": ["Both resume text and job description must be provided."],
            "explanation": "No text provided for analysis."
        }

    # 1. TF-IDF Cosine Similarity (Unigram for accurate vocabulary overlap)
    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 1), stop_words='english', sublinear_tf=True)
        tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_job])
        cosine_sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
    except Exception:
        cosine_sim = 0.35

    # 2. Extract genuine technical and domain keywords from JD
    job_keywords = extract_key_phrases_from_job(job_text, top_k=25)

    matched = []
    missing = []

    res_lower = " " + resume_text.lower() + " "

    for kw in job_keywords:
        kw_clean = kw.lower()
        if kw_clean in ["c", "r"]:
            pattern = rf"(?<![a-zA-Z0-9_]){re.escape(kw_clean)}(?![a-zA-Z0-9_])"
        else:
            pattern = rf"\b{re.escape(kw_clean)}\b"

        if re.search(pattern, res_lower):
            matched.append(kw)
        else:
            missing.append(kw)

    total_kw = len(job_keywords)
    keyword_match_pct = (len(matched) / total_kw * 100.0) if total_kw > 0 else 0.0

    # 3. Scaled Cosine Similarity
    # In NLP cosine similarity between resume and job description, 0.40+ represents top-tier overlap.
    cosine_sim_pct = min(100.0, cosine_sim * 100.0 * 2.0)

    # 4. Composite ATS Score (60% keyword coverage + 40% semantic cosine alignment)
    raw_score = (0.60 * keyword_match_pct) + (0.40 * cosine_sim_pct)
    match_score = round(max(5.0, min(98.0, raw_score)), 1)

    # 5. Tailored Recommendations
    recommendations = []
    if missing:
        missing_sample = ", ".join(missing[:5])
        recommendations.append(f"Incorporate missing core job keywords into your experience/projects: **{missing_sample}**.")

    if cosine_sim < 0.25:
        recommendations.append("Low overall semantic overlap: Align your summary and project descriptions more closely with the target domain phrasing.")
    elif cosine_sim >= 0.40:
        recommendations.append("Strong semantic alignment: Your terminology closely mirrors the employer's expectations.")

    if keyword_match_pct < 60.0:
        recommendations.append("Crucial requirement gaps detected: Emphasize practical experience with the employer's listed tools and methodologies.")
    else:
        recommendations.append("Solid keyword coverage: Your profile hits more than 60% of the critical requirements.")

    recommendations.append("Always integrate keywords naturally inside bullet points showcasing actual usage and outcomes; avoid keyword stuffing.")

    # 6. Clear Explanation
    if match_score >= 75.0:
        rating_tier = "Excellent Match (High Interview Probability)"
    elif match_score >= 55.0:
        rating_tier = "Good Match (Competitive with minor gaps)"
    elif match_score >= 40.0:
        rating_tier = "Moderate Match (Noticeable keyword gaps)"
    else:
        rating_tier = "Low Match (Substantial customization required)"

    explanation = (
        f"**{rating_tier}**: The overall ATS match score of **{match_score}%** is computed using two industry-standard metrics: "
        f"1) **Cosine Similarity ({round(cosine_sim, 2)})**, measuring holistic vocabulary and thematic alignment, "
        f"and 2) **Keyword Density ({round(keyword_match_pct, 1)}%)**, measuring exact matches of target requirements "
        f"({len(matched)} matched out of {total_kw} core keywords identified in the job description)."
    )

    return {
        "job_title": job_title,
        "match_score": match_score,
        "cosine_similarity": round(cosine_sim, 3),
        "keyword_match_pct": round(keyword_match_pct, 1),
        "total_keywords_analyzed": total_kw,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "recommendations": recommendations,
        "explanation": explanation
    }

"""
Career Engine module for Career AI.
Powers Skill Gap Analysis, Role Benchmarking, Career Roadmaps, and Comprehensive Reports.
"""

from typing import Dict, Any, List, Tuple
from ai_service import generate_career_roadmap

# Standard industry role skill benchmarks with priority tiers
ROLE_SKILL_BENCHMARKS = {
    "Full Stack Developer": {
        "High Priority": ["JavaScript", "Python", "React", "Node.js", "SQL", "Git", "REST API"],
        "Medium Priority": ["PostgreSQL", "Docker", "TypeScript", "Express", "HTML/CSS", "Unit Testing"],
        "Low Priority": ["Redis", "AWS", "CI/CD", "GraphQL", "Tailwind"]
    },
    "Frontend Developer": {
        "High Priority": ["JavaScript", "React", "TypeScript", "HTML/CSS", "Git", "REST API"],
        "Medium Priority": ["Next.js", "Tailwind", "Responsive Design", "State Management", "Unit Testing"],
        "Low Priority": ["GraphQL", "Webpack/Vite", "Figma", "WebSockets"]
    },
    "Backend Developer": {
        "High Priority": ["Python", "Java", "SQL", "REST API", "Git", "PostgreSQL", "Data Structures"],
        "Medium Priority": ["Docker", "FastAPI", "Django", "Spring Boot", "Redis", "Microservices"],
        "Low Priority": ["Kubernetes", "AWS", "Kafka", "CI/CD", "GraphQL"]
    },
    "Data Scientist": {
        "High Priority": ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Statistics"],
        "Medium Priority": ["Machine Learning", "Data Visualization", "Git", "Matplotlib/Plotly", "Feature Engineering"],
        "Low Priority": ["Deep Learning", "PyTorch", "TensorFlow", "Docker", "Big Data", "FastAPI"]
    },
    "Machine Learning Engineer": {
        "High Priority": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "Machine Learning", "Mathematics"],
        "Medium Priority": ["Docker", "SQL", "FastAPI", "Deep Learning", "NLP", "Computer Vision"],
        "Low Priority": ["Kubernetes", "MLflow", "ONNX", "Cloud (AWS/GCP)", "CI/CD"]
    },
    "DevOps / Cloud Engineer": {
        "High Priority": ["Linux", "Docker", "Git", "CI/CD", "AWS", "Bash / Shell"],
        "Medium Priority": ["Kubernetes", "Terraform", "GitHub Actions", "Networking", "Python"],
        "Low Priority": ["Ansible", "Prometheus", "Grafana", "Security / IAM", "ArgoCD"]
    },
    "Data Analyst": {
        "High Priority": ["SQL", "Excel", "Python", "Data Visualization", "Statistics"],
        "Medium Priority": ["Pandas", "Power BI", "Tableau", "Git", "Business Intelligence"],
        "Low Priority": ["NumPy", "R", "Machine Learning", "Database Modeling"]
    },
    "Cyber Security Analyst": {
        "High Priority": ["Networking", "Linux", "Security Fundamentals", "Vulnerability Assessment", "Firewalls"],
        "Medium Priority": ["Python", "SIEM Tools", "Wireshark", "Incident Response", "Penetration Testing"],
        "Low Priority": ["Cryptography", "Cloud Security", "Reverse Engineering", "Docker"]
    }
}


def analyze_skill_gap(current_skills: List[str], target_role: str) -> Dict[str, Any]:
    """
    Compares candidate's skills against standard role benchmark.
    Returns acquired vs missing skills categorized by priority,
    readiness score, and prioritized learning advice.
    """
    benchmark = ROLE_SKILL_BENCHMARKS.get(target_role)
    if not benchmark:
        # Default benchmark for unrecognized roles
        benchmark = {
            "High Priority": ["Git", "Problem Solving", "Core Programming", "System Fundamentals"],
            "Medium Priority": ["Database / SQL", "API Design", "Testing", "Documentation"],
            "Low Priority": ["Cloud Basics", "Docker", "Agile / Scrum"]
        }

    # Normalize candidate skills
    normalized_current = {s.strip().lower() for s in current_skills if s.strip()}

    acquired_skills = []
    missing_by_priority = {
        "High Priority": [],
        "Medium Priority": [],
        "Low Priority": []
    }

    total_weighted_points = 0.0
    earned_weighted_points = 0.0

    weights = {"High Priority": 3.0, "Medium Priority": 2.0, "Low Priority": 1.0}

    for priority, skills in benchmark.items():
        w = weights[priority]
        for skill in skills:
            total_weighted_points += w
            # Check match
            s_lower = skill.lower()
            if any(s_lower == cur or s_lower in cur or cur in s_lower for cur in normalized_current):
                acquired_skills.append(skill)
                earned_weighted_points += w
            else:
                missing_by_priority[priority].append(skill)

    readiness_score = 0.0
    if total_weighted_points > 0:
        readiness_score = round((earned_weighted_points / total_weighted_points) * 100.0, 1)

    # Formulate "What to Learn First" recommendations
    learn_first = []
    if missing_by_priority["High Priority"]:
        top_high = missing_by_priority["High Priority"][:3]
        learn_first.append(f"Immediate Core Focus: Master **{', '.join(top_high)}**. These are non-negotiable for {target_role}.")
    if missing_by_priority["Medium Priority"]:
        top_med = missing_by_priority["Medium Priority"][:3]
        learn_first.append(f"Secondary Stack Expansion: Learn **{', '.join(top_med)}** through hands-on project implementations.")
    if missing_by_priority["Low Priority"]:
        learn_first.append(f"Value-Add Differentiators: Build familiarity with **{', '.join(missing_by_priority['Low Priority'][:2])}** to stand out in interviews.")

    if not learn_first:
        learn_first.append("You match all benchmark skills for this role! Focus on system design and portfolio polish.")

    return {
        "target_role": target_role,
        "readiness_score": readiness_score,
        "benchmark_skills": benchmark,
        "acquired_skills": sorted(list(set(acquired_skills))),
        "missing_skills": missing_by_priority,
        "total_required": sum(len(skills) for skills in benchmark.values()),
        "total_acquired": len(set(acquired_skills)),
        "recommendations": learn_first
    }


def compile_career_report(candidate_name: str, target_role: str,
                          resume_data: Dict[str, Any] = None,
                          ats_data: Dict[str, Any] = None,
                          interview_data: Dict[str, Any] = None,
                          skill_gap_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Compiles an all-in-one comprehensive career readiness evaluation report.
    """
    resume_score = resume_data.get("quality_score") if resume_data else None
    ats_score = ats_data.get("match_score") if ats_data else None
    interview_score = interview_data.get("total_score") if interview_data else None
    readiness_score = skill_gap_data.get("readiness_score") if skill_gap_data else None

    # Calculate Composite Employability Index
    active_scores = [s for s in [resume_score, ats_score, interview_score, readiness_score] if s is not None]
    composite_index = round(sum(active_scores) / len(active_scores), 1) if active_scores else 50.0

    # Executive tier evaluation
    if composite_index >= 80.0:
        readiness_tier = "Job Ready (High Competitive Standing)"
        summary_tone = "shows outstanding preparation with robust technical capability and presentation."
    elif composite_index >= 65.0:
        readiness_tier = "Promising Candidate (Targeted Up-skilling Required)"
        summary_tone = "has a strong foundational baseline with clear opportunities to polish specific technical gaps."
    else:
        readiness_tier = "Emerging Learner (Development Stage)"
        summary_tone = "is in the foundational phase of career development. Focused roadmap execution is advised."

    executive_summary = (
        f"{candidate_name} is targeting the role of **{target_role}** with an overall "
        f"Employability Index of **{composite_index}%** ({readiness_tier}). "
        f"The candidate {summary_tone}"
    )

    # Detailed action items
    action_items = []
    if resume_score and resume_score < 75.0:
        action_items.append("Revise resume structure: integrate measurable metrics and ensure all essential sections are represented.")
    if ats_score and ats_score < 70.0:
        action_items.append("Tailor application materials: incorporate critical job description keywords into project descriptions.")
    if interview_score and interview_score < 70.0:
        action_items.append("Strengthen interview responses: use the STAR method to structure technical and behavioral answers.")
    if skill_gap_data and skill_gap_data.get("missing_skills", {}).get("High Priority"):
        high_gaps = skill_gap_data["missing_skills"]["High Priority"][:3]
        action_items.append(f"Prioritize acquiring top missing competencies: {', '.join(high_gaps)}.")

    if not action_items:
        action_items.append("Maintain momentum by contributing to open-source software and participating in mock technical screens.")

    report = {
        "candidate_name": candidate_name,
        "target_role": target_role,
        "composite_index": composite_index,
        "readiness_tier": readiness_tier,
        "executive_summary": executive_summary,
        "resume_score": resume_score,
        "ats_score": ats_score,
        "interview_score": interview_score,
        "skill_readiness_score": readiness_score,
        "action_items": action_items,
        "resume_data": resume_data,
        "ats_data": ats_data,
        "interview_data": interview_data,
        "skill_gap_data": skill_gap_data
    }

    return report

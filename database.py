"""
Database module for Career AI.
Manages SQLite storage for resumes, ATS analyses, mock interviews, skill gaps, and reports.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "career_ai.db")


def get_connection():
    """Returns a SQLite connection with row factory enabled."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes all required database tables if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Resumes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                upload_timestamp TEXT NOT NULL,
                raw_text TEXT NOT NULL,
                sections_json TEXT NOT NULL,
                skills_json TEXT NOT NULL,
                quality_score REAL NOT NULL,
                suggestions_json TEXT NOT NULL
            )
        """)

        # ATS Analyses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ats_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                match_score REAL NOT NULL,
                cosine_sim REAL NOT NULL,
                keyword_match_pct REAL NOT NULL,
                matched_keywords_json TEXT NOT NULL,
                missing_keywords_json TEXT NOT NULL,
                recommendations_json TEXT NOT NULL
            )
        """)

        # Mock Interview sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interview_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                category TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                total_score REAL NOT NULL,
                strengths TEXT NOT NULL,
                weaknesses TEXT NOT NULL,
                suggestions TEXT NOT NULL,
                qa_details_json TEXT NOT NULL
            )
        """)

        # Skill Gap Analysis table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skill_gap_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_role TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                current_skills_json TEXT NOT NULL,
                missing_skills_json TEXT NOT NULL,
                priority_json TEXT NOT NULL,
                readiness_score REAL NOT NULL
            )
        """)

        # Career Reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS career_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_name TEXT NOT NULL,
                target_role TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                resume_score REAL,
                ats_score REAL,
                interview_score REAL,
                readiness_score REAL,
                summary_text TEXT NOT NULL,
                report_json TEXT NOT NULL
            )
        """)

        conn.commit()


# --- Resume Operations ---
def save_resume_analysis(filename: str, raw_text: str, sections: dict, skills: list,
                         quality_score: float, suggestions: list) -> int:
    """Saves a resume analysis record and returns the new row ID."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO resumes (filename, upload_timestamp, raw_text, sections_json, skills_json, quality_score, suggestions_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            filename,
            now,
            raw_text,
            json.dumps(sections),
            json.dumps(skills),
            round(quality_score, 1),
            json.dumps(suggestions)
        ))
        conn.commit()
        return cursor.lastrowid


def get_latest_resume() -> Optional[Dict[str, Any]]:
    """Fetches the most recent resume analysis."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM resumes ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "filename": row["filename"],
            "upload_timestamp": row["upload_timestamp"],
            "raw_text": row["raw_text"],
            "sections": json.loads(row["sections_json"]),
            "skills": json.loads(row["skills_json"]),
            "quality_score": row["quality_score"],
            "suggestions": json.loads(row["suggestions_json"])
        }


def get_all_resumes(limit: int = 10) -> List[Dict[str, Any]]:
    """Fetches recent resumes."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename, upload_timestamp, quality_score FROM resumes ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in cursor.fetchall()]


# --- ATS Operations ---
def save_ats_analysis(resume_name: str, job_title: str, match_score: float,
                      cosine_sim: float, keyword_match_pct: float,
                      matched_keywords: list, missing_keywords: list,
                      recommendations: list) -> int:
    """Saves an ATS analysis record."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ats_analyses (resume_name, job_title, timestamp, match_score, cosine_sim, keyword_match_pct, matched_keywords_json, missing_keywords_json, recommendations_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            resume_name,
            job_title,
            now,
            round(match_score, 1),
            round(cosine_sim, 3),
            round(keyword_match_pct, 1),
            json.dumps(matched_keywords),
            json.dumps(missing_keywords),
            json.dumps(recommendations)
        ))
        conn.commit()
        return cursor.lastrowid


def get_latest_ats_analysis() -> Optional[Dict[str, Any]]:
    """Fetches the latest ATS record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ats_analyses ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "resume_name": row["resume_name"],
            "job_title": row["job_title"],
            "timestamp": row["timestamp"],
            "match_score": row["match_score"],
            "cosine_sim": row["cosine_sim"],
            "keyword_match_pct": row["keyword_match_pct"],
            "matched_keywords": json.loads(row["matched_keywords_json"]),
            "missing_keywords": json.loads(row["missing_keywords_json"]),
            "recommendations": json.loads(row["recommendations_json"])
        }


# --- Mock Interview Operations ---
def save_interview_session(role: str, category: str, total_score: float,
                           strengths: str, weaknesses: str, suggestions: str,
                           qa_details: list) -> int:
    """Saves an interview session evaluation."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO interview_sessions (role, category, timestamp, total_score, strengths, weaknesses, suggestions, qa_details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            role,
            category,
            now,
            round(total_score, 1),
            strengths,
            weaknesses,
            suggestions,
            json.dumps(qa_details)
        ))
        conn.commit()
        return cursor.lastrowid


def get_recent_interviews(limit: int = 10) -> List[Dict[str, Any]]:
    """Fetches past interview sessions."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM interview_sessions ORDER BY id DESC LIMIT ?", (limit,))
        results = []
        for row in cursor.fetchall():
            item = dict(row)
            item["qa_details"] = json.loads(item["qa_details_json"])
            results.append(item)
        return results


def get_latest_interview() -> Optional[Dict[str, Any]]:
    """Fetches the latest interview session."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM interview_sessions ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return None
        item = dict(row)
        item["qa_details"] = json.loads(item["qa_details_json"])
        return item


# --- Skill Gap Operations ---
def save_skill_gap_analysis(target_role: str, current_skills: list,
                            missing_skills: list, priority_map: dict,
                            readiness_score: float) -> int:
    """Saves a skill gap analysis record."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO skill_gap_records (target_role, timestamp, current_skills_json, missing_skills_json, priority_json, readiness_score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            target_role,
            now,
            json.dumps(current_skills),
            json.dumps(missing_skills),
            json.dumps(priority_map),
            round(readiness_score, 1)
        ))
        conn.commit()
        return cursor.lastrowid


def get_latest_skill_gap() -> Optional[Dict[str, Any]]:
    """Fetches the latest skill gap record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM skill_gap_records ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "target_role": row["target_role"],
            "timestamp": row["timestamp"],
            "current_skills": json.loads(row["current_skills_json"]),
            "missing_skills": json.loads(row["missing_skills_json"]),
            "priority_map": json.loads(row["priority_json"]),
            "readiness_score": row["readiness_score"]
        }


# --- Career Report Operations ---
def save_career_report(candidate_name: str, target_role: str, resume_score: Optional[float],
                       ats_score: Optional[float], interview_score: Optional[float],
                       readiness_score: Optional[float], summary_text: str, report_dict: dict) -> int:
    """Saves a compiled career report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO career_reports (candidate_name, target_role, timestamp, resume_score, ats_score, interview_score, readiness_score, summary_text, report_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            candidate_name,
            target_role,
            now,
            resume_score,
            ats_score,
            interview_score,
            readiness_score,
            summary_text,
            json.dumps(report_dict)
        ))
        conn.commit()
        return cursor.lastrowid


# --- Dashboard Aggregation ---
def get_dashboard_metrics() -> Dict[str, Any]:
    """Retrieves high-level summary metrics across all activities."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM resumes")
        total_resumes = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(quality_score) FROM resumes")
        avg_resume_score = cursor.fetchone()[0] or 0.0

        cursor.execute("SELECT COUNT(*) FROM ats_analyses")
        total_ats = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(match_score) FROM ats_analyses")
        avg_ats_score = cursor.fetchone()[0] or 0.0

        cursor.execute("SELECT COUNT(*) FROM interview_sessions")
        total_interviews = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(total_score) FROM interview_sessions")
        avg_interview_score = cursor.fetchone()[0] or 0.0

        cursor.execute("SELECT COUNT(*) FROM skill_gap_records")
        total_skill_gaps = cursor.fetchone()[0]

        # Recent activities log
        cursor.execute("""
            SELECT 'Resume Analyzed' as type, filename as label, upload_timestamp as time, quality_score as score
            FROM resumes
            UNION ALL
            SELECT 'ATS Checked' as type, job_title as label, timestamp as time, match_score as score
            FROM ats_analyses
            UNION ALL
            SELECT 'Mock Interview' as type, role as label, timestamp as time, total_score as score
            FROM interview_sessions
            ORDER BY time DESC LIMIT 6
        """)
        recent_activity = [dict(row) for row in cursor.fetchall()]

        return {
            "total_resumes": total_resumes,
            "avg_resume_score": round(avg_resume_score, 1),
            "total_ats": total_ats,
            "avg_ats_score": round(avg_ats_score, 1),
            "total_interviews": total_interviews,
            "avg_interview_score": round(avg_interview_score, 1),
            "total_skill_gaps": total_skill_gaps,
            "recent_activity": recent_activity
        }


# Auto-initialize database schema on module import
init_db()

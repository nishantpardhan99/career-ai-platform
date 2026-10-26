"""
Automated Test Suite for Career AI Platform.
Tests database, resume analyzer, ATS engine, AI service, and career engine.
"""

import os
import sys
import database
import ai_service
import resume_analyzer
import ats_engine
import career_engine

def run_tests():
    print("=" * 60)
    print("RUNNING COMPLETE AUTOMATED TEST SUITE FOR CAREER AI")
    print("=" * 60)

    # 1. Database tests
    print("\n[TEST 1] Testing Database Operations...")
    database.init_db()
    
    # Save dummy resume
    res_id = database.save_resume_analysis(
        filename="test_resume.pdf",
        raw_text="Test resume content with Python and SQL",
        sections={"Skills": True, "Education": True},
        skills=["Python", "SQL"],
        quality_score=85.0,
        suggestions=["Add GitHub URL"]
    )
    assert res_id > 0, "Failed to save resume analysis"
    latest_res = database.get_latest_resume()
    assert latest_res is not None, "Failed to fetch latest resume"
    assert latest_res["quality_score"] == 85.0, "Resume score mismatch"
    print("[OK] Database resume operations: PASSED")

    # Save ATS analysis
    ats_id = database.save_ats_analysis(
        resume_name="test_resume.pdf",
        job_title="Software Engineer",
        match_score=78.5,
        cosine_sim=0.62,
        keyword_match_pct=80.0,
        matched_keywords=["Python", "SQL"],
        missing_keywords=["Docker"],
        recommendations=["Add Docker experience"]
    )
    assert ats_id > 0, "Failed to save ATS analysis"
    latest_ats = database.get_latest_ats_analysis()
    assert latest_ats is not None, "Failed to fetch latest ATS analysis"
    assert latest_ats["match_score"] == 78.5, "ATS score mismatch"
    print("[OK] Database ATS operations: PASSED")

    # Save Interview
    inv_id = database.save_interview_session(
        role="Software Engineer",
        category="Technical",
        total_score=82.0,
        strengths="Clear STAR explanation",
        weaknesses="Brief on indexing",
        suggestions="Quantify latency improvement",
        qa_details=[{"q": "What is REST?", "a": "Architectural style", "score": 82.0}]
    )
    assert inv_id > 0, "Failed to save interview session"
    latest_inv = database.get_latest_interview()
    assert latest_inv is not None, "Failed to fetch latest interview"
    print("[OK] Database interview operations: PASSED")

    # Save Skill Gap
    sg_id = database.save_skill_gap_analysis(
        target_role="Full Stack Developer",
        current_skills=["Python", "SQL"],
        missing_skills=["React", "Docker"],
        priority_map={"High Priority": ["React"]},
        readiness_score=65.0
    )
    assert sg_id > 0, "Failed to save skill gap analysis"
    print("[OK] Database skill gap operations: PASSED")

    # Dashboard Metrics
    metrics = database.get_dashboard_metrics()
    assert metrics["total_resumes"] >= 1, "Metrics count failed"
    print("[OK] Database dashboard aggregation: PASSED")

    # 2. Resume Analyzer tests
    print("\n[TEST 2] Testing Resume Analyzer...")
    sample_text = """
    Jane Smith
    jane.smith@email.com | +1 555-123-4567 | github.com/janesmith | linkedin.com/in/janesmith
    
    PROFESSIONAL SUMMARY
    Senior Software Engineer with 4 years building web apps.
    
    WORK EXPERIENCE
    Software Engineer | Tech Corp
    • Architected microservices with Python, FastAPI and PostgreSQL, reducing latency by 45%.
    • Spearheaded frontend features in React and TypeScript for 20,000+ active users.
    
    EDUCATION
    BS in Computer Science, State University
    
    SKILLS
    Python, React, TypeScript, PostgreSQL, Docker, Git, REST API
    
    PROJECTS
    • TaskTracker: Built collaborative agile board with WebSockets and Redis.
    """
    res_audit = resume_analyzer.analyze_resume_text(sample_text, "Jane_Smith_Resume.pdf")
    assert res_audit["quality_score"] > 60, f"Expected high quality score, got {res_audit['quality_score']}"
    assert "Python" in res_audit["skills"], "Failed to extract Python skill"
    assert "React" in res_audit["skills"], "Failed to extract React skill"
    assert res_audit["sections"]["Work Experience"] is True, "Failed to detect Work Experience section"
    print(f"[OK] Resume Analyzer audit: PASSED (Quality Score: {res_audit['quality_score']}%, Skills: {len(res_audit['skills'])})")

    # 3. ATS Engine tests
    print("\n[TEST 3] Testing ATS Engine...")
    job_desc = """
    Software Engineer needed. Requirements: Strong experience in Python, FastAPI, Docker, and PostgreSQL.
    Must understand microservices architecture, REST APIs, and unit testing.
    """
    ats_res = ats_engine.calculate_ats_match(sample_text, job_desc, "Software Engineer")
    assert ats_res["match_score"] > 40, f"Expected reasonable ATS score, got {ats_res['match_score']}"
    assert len(ats_res["matched_keywords"]) > 0, "Expected matched keywords"
    assert "explanation" in ats_res, "Expected explanation in ATS result"
    print(f"[OK] ATS Engine match: PASSED (Match Score: {ats_res['match_score']}%, Matched: {len(ats_res['matched_keywords'])})")

    # 4. AI Service & Fallbacks
    print("\n[TEST 4] Testing AI Service & Fallback Mechanisms...")
    status = ai_service.check_ollama_status()
    print(f"  AI Status Message: {status['message']}")
    
    # Test resume improvement fallback
    imp_bullets = ai_service.improve_resume_text("worked on database queries and handled bugs", mode="bullet_points")
    assert "enhanced_text" in imp_bullets, "Improvement text missing"
    assert "Engineered" in imp_bullets["enhanced_text"] or "Architected" in imp_bullets["enhanced_text"] or "Managed" in imp_bullets["enhanced_text"], "Action verb replacement missing"
    print("[OK] AI Resume Improver (Bullet Points Fallback): PASSED")

    # Test grammar polish
    imp_gram = ai_service.improve_resume_text("in order to fix bugs due to the fact that we had errors", mode="grammar_clarity")
    assert "to fix bugs" in imp_gram["enhanced_text"] or "because" in imp_gram["enhanced_text"], "Grammar cleanup failed"
    print("[OK] AI Resume Improver (Grammar Clarity Fallback): PASSED")

    # Test interview evaluator fallback
    int_eval = ai_service.evaluate_interview_answer(
        question="How do you optimize a slow database query?",
        answer="In my previous project, we had queries taking over 2 seconds. I analyzed the execution plan with EXPLAIN, added indexes on key foreign columns, and introduced caching. This reduced query latency by 70%.",
        category="Technical",
        role="Software Engineer"
    )
    assert int_eval["score"] >= 65, f"Expected good score for STAR answer, got {int_eval['score']}"
    assert len(int_eval["strengths"]) > 0, "Expected strengths listed"
    print(f"[OK] AI Interview Answer Evaluator: PASSED (Score: {int_eval['score']}%)")

    # Test career roadmap fallback
    rm = ai_service.generate_career_roadmap(role="Software Engineer", level="Beginner")
    assert len(rm["phases"]) == 3, "Expected 3 roadmap phases"
    print("[OK] AI Career Roadmap Generator: PASSED")

    # 5. Career Engine tests
    print("\n[TEST 5] Testing Career Engine...")
    user_skills = ["Python", "SQL", "Git"]
    gap = career_engine.analyze_skill_gap(user_skills, "Full Stack Developer")
    assert gap["readiness_score"] > 0, "Readiness score should be > 0"
    assert len(gap["missing_skills"]["High Priority"]) > 0, "Expected missing high priority skills"
    print(f"[OK] Skill Gap Analyzer: PASSED (Readiness: {gap['readiness_score']}%)")

    # Master Report compilation
    rep = career_engine.compile_career_report("Jane Smith", "Software Engineer", res_audit, ats_res, {"total_score": 85.0}, gap)
    assert rep["composite_index"] > 50, "Expected valid composite index"
    assert len(rep["action_items"]) > 0, "Expected actionable items in report"
    print(f"[OK] Career Report Compiler: PASSED (Employability Index: {rep['composite_index']}%)")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! THE APPLICATION ENGINE IS 100% READY.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()

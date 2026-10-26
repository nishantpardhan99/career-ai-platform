"""
Career AI - AI-Powered Career Development Platform
Main Streamlit Application & Dashboard
"""

import streamlit as st
import database
import ai_service
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Career AI - Career Development Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6366F1, #A855F7, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #94A3B8;
        margin-bottom: 2rem;
    }
    .status-card {
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        background-color: #1E293B;
        border: 1px solid #334155;
        margin-bottom: 1.5rem;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 12px;
        background-color: #1E293B;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
    }
    .feature-card:hover {
        border-color: #6366F1;
        transform: translateY(-2px);
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-online {
        background-color: #065F46;
        color: #34D399;
    }
    .badge-offline {
        background-color: #374151;
        color: #9CA3AF;
    }
    .stMetric {
        background-color: #1E293B;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# Ensure Database is Ready
database.init_db()

# Sidebar: Profile & Global State
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1534972195531-a756b1126f24?w=600&auto=format&fit=crop&q=80", use_container_width=True)
    st.title("🎯 Career AI")
    st.caption("College Minor Project • Production MVP")

    st.markdown("---")
    st.subheader("Candidate Profile")
    if "candidate_name" not in st.session_state:
        st.session_state.candidate_name = "Alex Johnson"
    if "target_role" not in st.session_state:
        st.session_state.target_role = "Full Stack Developer"

    cand_name = st.text_input("Name", value=st.session_state.candidate_name)
    target_role = st.selectbox(
        "Target Role",
        [
            "Full Stack Developer",
            "Frontend Developer",
            "Backend Developer",
            "Data Scientist",
            "Machine Learning Engineer",
            "DevOps / Cloud Engineer",
            "Data Analyst",
            "Cyber Security Analyst"
        ],
        index=0
    )
    st.session_state.candidate_name = cand_name
    st.session_state.target_role = target_role

    st.markdown("---")
    st.subheader("System Diagnostics")
    ollama_info = ai_service.check_ollama_status()
    if ollama_info["available"] and ollama_info["models"]:
        st.markdown(f'<span class="badge badge-online">● Ollama Connected</span>', unsafe_allow_html=True)
        st.caption(f"Active Model: `{ollama_info['active_model']}`")
    else:
        st.markdown(f'<span class="badge badge-offline">○ Offline Fallback Active</span>', unsafe_allow_html=True)
        st.caption("Using deterministic NLP & heuristic engines.")

    st.caption("Database: SQLite (`career_ai.db`)")


# Main Dashboard Content
st.markdown('<div class="main-header">Career AI Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Career Development Platform with Resume Analysis, ATS Matching & Mock Interviews</div>', unsafe_allow_html=True)

# System Status Banner
status = ai_service.check_ollama_status()
col_stat1, col_stat2 = st.columns([3, 1])
with col_stat1:
    st.info(f"💡 **AI Engine Status:** {status['message']}")
with col_stat2:
    if st.button("🔄 Refresh AI Status", use_container_width=True):
        st.rerun()

# Overview Metrics from Database
metrics = database.get_dashboard_metrics()
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="📄 Resumes Evaluated", value=metrics["total_resumes"], delta=f"Avg Score: {metrics['avg_resume_score']}%" if metrics["total_resumes"] > 0 else None)
with m2:
    st.metric(label="🎯 ATS Job Matches", value=metrics["total_ats"], delta=f"Avg Match: {metrics['avg_ats_score']}%" if metrics["total_ats"] > 0 else None)
with m3:
    st.metric(label="🎙️ Mock Interviews", value=metrics["total_interviews"], delta=f"Avg Score: {metrics['avg_interview_score']}%" if metrics["total_interviews"] > 0 else None)
with m4:
    st.metric(label="📊 Skill Gap Analyses", value=metrics["total_skill_gaps"])

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Cards to Core Modules
st.subheader("🚀 Platform Modules")
st.markdown("Navigate to any module from the sidebar or click into the tools below:")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature-card">
        <h3>1. 📄 Resume Analyzer</h3>
        <p>Upload your PDF resume to extract raw text with PyMuPDF, audit structural sections, extract technical skills, and calculate a comprehensive quality score.</p>
        <p><strong>Highlights:</strong> Section detection, zero-hallucination skill taxonomy, contact checker.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Resume Analyzer", key="btn_p1", use_container_width=True):
        st.switch_page("pages/1_Resume_Analyzer.py")

with c2:
    st.markdown("""
    <div class="feature-card">
        <h3>2. 🎯 ATS Checker</h3>
        <p>Benchmark your resume against specific target job descriptions using TF-IDF vectorization and cosine similarity to discover keyword matches and gaps.</p>
        <p><strong>Highlights:</strong> Hybrid match scoring, matched vs missing keywords, ranking explanation.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open ATS Checker", key="btn_p2", use_container_width=True):
        st.switch_page("pages/2_ATS_Checker.py")

with c3:
    st.markdown("""
    <div class="feature-card">
        <h3>3. ✍️ AI Resume Improver</h3>
        <p>Enhance bullet points using executive power verbs, improve professional clarity, eliminate filler phrases, and polish your candidate summary.</p>
        <p><strong>Highlights:</strong> Ollama LLM integration, rule-based transformation engine fallback.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open AI Resume Improver", key="btn_p3", use_container_width=True):
        st.switch_page("pages/3_AI_Resume_Improver.py")

st.markdown("<br>", unsafe_allow_html=True)

c4, c5, c6 = st.columns(3)

with c4:
    st.markdown("""
    <div class="feature-card">
        <h3>4. 🎙️ AI Mock Interview</h3>
        <p>Practice role-tailored technical and HR interview questions. Type your answers and receive immediate scores, strengths, weaknesses, and STAR feedback.</p>
        <p><strong>Highlights:</strong> Technical & HR questions, STAR method evaluation, SQLite history.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Mock Interview", key="btn_p4", use_container_width=True):
        st.switch_page("pages/4_Mock_Interview.py")

with c5:
    st.markdown("""
    <div class="feature-card">
        <h3>5. 🔍 Skill Gap Analyzer</h3>
        <p>Benchmark your current skill inventory against standard industry role requirements. Categorizes missing skills into High, Medium, and Low priorities.</p>
        <p><strong>Highlights:</strong> Readiness score, priority categorization, learning order advice.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Skill Gap Analyzer", key="btn_p5", use_container_width=True):
        st.switch_page("pages/5_Skill_Gap.py")

with c6:
    st.markdown("""
    <div class="feature-card">
        <h3>6. 🗺️ Career Roadmap</h3>
        <p>Generate a phased 3-tier milestone learning plan (Beginner → Intermediate → Advanced) featuring curated project ideas and verified learning resources.</p>
        <p><strong>Highlights:</strong> Structured timeline, milestone projects, Ollama/deterministic modes.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Career Roadmap", key="btn_p6", use_container_width=True):
        st.switch_page("pages/6_Career_Roadmap.py")

st.markdown("<br>", unsafe_allow_html=True)

# Master Report Banner
st.markdown("""
<div style="background: linear-gradient(135deg, #1E1B4B, #312E81); padding: 1.8rem; border-radius: 12px; border: 1px solid #4338CA;">
    <h3 style="margin-top:0;">📊 7. Career Readiness Report</h3>
    <p>Consolidate your resume audit, ATS scan, mock interview results, and skill gaps into an executive employability summary with downloadable markdown & HTML exports.</p>
</div>
""", unsafe_allow_html=True)
if st.button("View Comprehensive Career Report", key="btn_p7", use_container_width=True):
    st.switch_page("pages/7_Career_Report.py")

# Recent Activity Section
st.markdown("---")
st.subheader("🕒 Recent Activity Feed")

if metrics["recent_activity"]:
    act_df = pd.DataFrame(metrics["recent_activity"])
    act_df.columns = ["Activity Type", "Subject / Label", "Timestamp", "Score Achieved"]
    st.dataframe(act_df, use_container_width=True, hide_index=True)
else:
    st.info("No recorded activity yet. Start by uploading a resume in the **Resume Analyzer** or taking a **Mock Interview**!")

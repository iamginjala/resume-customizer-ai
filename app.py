import streamlit as st
import json
from agents import job_analyzer, quality_checker, resume_writer
# from mock_agents import job_analyzer, quality_checker, resume_writer
from document_generator import pdf_generator, word_generator
import os


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))        # .../Job application assistant
db_path = os.path.join(PROJECT_ROOT, "DATA", "resume.db")


st.set_page_config(page_title="Resume Tailor", page_icon="📄", layout="wide")

# --- Auth Gate ---
if not st.user.is_logged_in:
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.title("📄 Resume Tailor")
        st.subheader("This app is private. Please log in to continue.")
        st.button("Log in with Google", on_click=st.login, type="primary")
    st.stop()

conn = st.connection("resume_db", type="sql", url=f"sqlite:///{db_path}")

# --- Sidebar: user + resume selection ---
with st.sidebar:
    st.markdown(f"**{st.user.name}**")
    st.caption(st.user.email)
    st.button("Log out", on_click=st.logout)

    st.divider()

    names_df = conn.query("select name from resumes;")

    selected = st.selectbox("Resume Template", names_df["name"])

resume_df = conn.query("select resume_json from resumes where name = :name;" , params= {"name": selected},)

raw_json_text = resume_df.iloc[0]["resume_json"]
selected_resume = json.loads(raw_json_text)

# --- Main content ---
st.title("📄 Resume Tailor")
st.caption(f"Welcome back, {(st.user.name or 'there').split()[0]}") # type: ignore


jd = st.text_area("Paste Job Description", height=300, placeholder="Paste the job description here...")

# --- Initialize Session State ---
# This ensures variables persist when the app reruns
if "resume_bytes" not in st.session_state:
    st.session_state.resume_bytes = None
if "word_bytes" not in st.session_state:
    st.session_state.word_bytes = None
if "usage_records" not in st.session_state:
    st.session_state.usage_records = []

# --- Action Button ---
if st.button("Generate Resume", type="primary"):
    if not jd.strip():
        st.error("Please paste a job description first.")
    else:
        with st.spinner("Working..."):
            records = []

            # 1. Analyze Job Description
            analysis, usage = job_analyzer.analyze(jd)
            records.append({"step": "Job Analysis", **usage})

            # 2. Iterate to customize resume
            MAX_ITERATIONS = 2
            feedback = None

            for i in range(MAX_ITERATIONS):
                customized_resume, usage = resume_writer.write(analysis, selected_resume, feedback) # type: ignore
                records.append({"step": f"Resume Writer (iter {i+1})", **usage})
                score, feedback, usage = quality_checker.check(customized_resume, analysis)
                records.append({"step": f"Quality Check (iter {i+1})", **usage})
                if score >= 7:
                    break

            # 3. Generate documents and SAVE to session_state
            st.session_state.resume_bytes = pdf_generator.generate(customized_resume)
            st.session_state.word_bytes = word_generator.generate(customized_resume)
            st.session_state.usage_records = records

            st.success("Resume generated!")

# --- Download Buttons ---
# Placed outside the "Generate" button block so they survive the page rerun
if st.session_state.resume_bytes and st.session_state.word_bytes:
    st.divider()
    st.subheader("Your tailored resume is ready")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Download PDF",
            data=st.session_state.resume_bytes,
            file_name="resume.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    with col2:
        st.download_button(
            label="Download Word",
            data=st.session_state.word_bytes,
            file_name="resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

if st.session_state.usage_records:
    with st.expander("Token Usage & Cost", expanded=False):
        total_input = total_output = total_cost = 0
        for rec in st.session_state.usage_records:
            total_input += rec["input_tokens"]
            total_output += rec["output_tokens"]
            total_cost += rec["cost"]
            st.markdown(
                f"**{rec['step']}** (`{rec['model']}`): "
                f"{rec['input_tokens']:,} in / {rec['output_tokens']:,} out — "
                f"**${rec['cost']:.4f}**"
            )
        st.divider()
        st.markdown(
            f"**Total**: {total_input:,} input tokens, {total_output:,} output tokens — "
            f"**${total_cost:.4f}**"
        )

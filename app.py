import streamlit as st 
import json 
from agents import job_analyzer, quality_checker, resume_writer
# from mock_agents import job_analyzer, quality_checker, resume_writer
from document_generator import pdf_generator, word_generator

# --- UI Setup ---
resume_options = {
    "Power Platform Resume": "resume_pp.json",
    "DevOps Resume": "resume_devops.json"
}

selected = st.selectbox("Select Resume", list(resume_options.keys()))

with open(resume_options[selected]) as f:
    selected_resume = json.load(f)

jd = st.text_area("Paste Job Description", height=300)

# --- Initialize Session State ---
# This ensures variables persist when the app reruns
if "resume_bytes" not in st.session_state:
    st.session_state.resume_bytes = None
if "word_bytes" not in st.session_state:
    st.session_state.word_bytes = None

# --- Action Button ---
if st.button("Generate Resume"):
    if not jd.strip():
        st.error("Please paste a job description first.")
    else:
        with st.spinner("Working..."):
            # 1. Analyze Job Description
            analysis = job_analyzer.analyze(jd)
            
            # 2. Iterate to customize resume
            MAX_ITERATIONS = 2
            feedback = None
            
            for i in range(MAX_ITERATIONS):
                customized_resume = resume_writer.write(analysis, selected_resume, feedback) # type: ignore
                score, feedback = quality_checker.check(customized_resume, analysis)
                if score >= 7:
                    break
            
            # 3. Generate documents and SAVE to session_state
            st.session_state.resume_bytes = pdf_generator.generate(customized_resume)
            st.session_state.word_bytes = word_generator.generate(customized_resume)
            
            st.success("Resume generated!")

# --- Download Buttons ---
# Placed outside the "Generate" button block so they survive the page rerun
if st.session_state.resume_bytes and st.session_state.word_bytes:
    
    # Putting buttons side-by-side looks a bit cleaner in Streamlit
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="Download PDF",
            data=st.session_state.resume_bytes,
            file_name="resume.pdf",
            mime="application/pdf"
        )
        
    with col2:
        st.download_button(
            label="Download Word",
            data=st.session_state.word_bytes,
            file_name="resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
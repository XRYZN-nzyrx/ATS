from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import fitz  # PyMuPDF
import google.generativeai as genai

#  Gemini AI setup
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#  Generate AI Response
def get_gemini_response(input_text, pdf_content, prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([input_text] + pdf_content + [prompt])
        return response.text
    except Exception as e:
        return f"❗ AI processing error: {e}"

#  Process PDF into image chunks
def input_pdf_setup(uploaded_file):
    if uploaded_file:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        pdf_parts = []
        for page in pdf_document:
            pix = page.get_pixmap()
            img_byte_arr = io.BytesIO(pix.tobytes("jpeg"))
            img_byte_arr.seek(0)
            pdf_parts.append({
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr.read()).decode()
            })
        return pdf_parts
    else:
        raise FileNotFoundError("No PDF uploaded")

#  Display Gemini Result in Markdown Format
def display_result(response_text):
    st.markdown("### 📊 ATS Evaluation Report")
    st.markdown(response_text)  # Render properly using Markdown

#  Streamlit App Config
st.set_page_config(page_title="ATS Resume Expert 2025+", layout="centered")
st.title("⚡ ATS Resume Analyzer — Future Ready")

#  Inputs
input_text = st.text_area("📋 Paste Job Description", key="job_desc")
uploaded_file = st.file_uploader("📄 Upload Resume (PDF only)", type=["pdf"])

if uploaded_file:
    st.success("Resume uploaded ✅")

#  Buttons
submit1 = st.button("🧠 Expert Resume Evaluation")
submit2 = st.button("📈 Skill Improvement Suggestions")
submit3 = st.button("📊 ATS Match Percentage")

#  Prompts
input_prompt1 = """
[Role]: Senior HR Analyst with AI-driven evaluation skills.
[Objective]: Review resume vs job description for high-tech roles in 2025+ including AI, full stack, MLOps, cloud-native, and data security fields.
[Criteria]:
- Emerging tech skills and real-world projects
- Certifications and learning trajectory
- Soft skills for hybrid, global teams
- Communication effectiveness and impact-driven achievements
[Output]:
- ✅ Verdict summary
- 🔍 Strengths
- ⚠️ Weaknesses
- 🧩 Suggestions
"""

input_prompt2 = """
[Role]: Career Coach for AI-era upskilling.
[Objective]: Analyze resume and job description to detect:
- Missing or outdated skills
- Suggested trending tools, platforms, or certifications
- Career path alignment
[Output]:
- 📌 Skills to improve
- 🛠️ Courses or resources
- 🚀 Career trajectory tips
"""

input_prompt3 = """
[Role]: Smart ATS evaluator for 2025 as well as for upcoming years tech hiring workflows.
[Objective]: Compare resume vs job role using keyword relevance, semantic matching, and role-fit logic.
[Output]:
- 🔢 Match Score (%)
- 📉 Missing Keywords
- 🧠 Observations
- ✅ Fit Summary
"""

#  Response Engine
if submit1:
    if uploaded_file:
        with st.spinner("Running expert analysis..."):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("🧠 Resume Evaluation")
            display_result(response)
    else:
        st.warning("Please upload your resume first.")

elif submit2:
    if uploaded_file:
        with st.spinner("Analyzing skills..."):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt2)
            st.subheader("📈 Skill Suggestions")
            display_result(response)
    else:
        st.warning("Please upload your resume first.")

elif submit3:
    if uploaded_file:
        with st.spinner("Scanning ATS metrics..."):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("📊 ATS Score")
            display_result(response)
    else:
        st.warning("Please upload your resume first.")

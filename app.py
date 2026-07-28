import os
import tempfile
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="AI Resume Assistant",
    page_icon="📄",
)

st.title("📄 AI Resume Assistant")
st.write("Analyse your CV with Google Gemini for the UK job market.")

if not api_key:
    st.error("API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

analysis_mode = st.selectbox(
    "Choose an analysis mode",
    [
        "General CV Analysis",
        "CV and Job Match",
        "CV Improvement Suggestions",
        "Interview Questions",
    ],
)

st.info(
    "Privacy notice: Your CV is processed only to generate the analysis. "
    "Avoid uploading documents containing unnecessary sensitive information."
)

st.caption(
    "AI-generated feedback is for guidance only and is not an official ATS assessment."
)
uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"],
)

job_description = ""

if analysis_mode == "CV and Job Match":
    job_description = st.text_area(
        "Paste the job description",
        height=200,
        placeholder="Paste the full job description here...",
    )

if uploaded_file:
    st.success("Resume uploaded successfully!")

    if st.button("Run Analysis"):
        if analysis_mode == "CV and Job Match" and not job_description.strip():
            st.warning("Please paste a job description first.")
            st.stop()

        prompts = {
            "General CV Analysis": """
You are an expert UK recruitment consultant.

Analyse the attached CV and provide:

1. Professional summary
2. Strongest skills
3. Weak or unclear areas
4. Structure and formatting feedback
5. Five specific improvements
6. Overall CV score out of 100

Do not invent experience, skills or qualifications.
""",
            "CV and Job Match": f"""
You are an expert UK recruitment consultant and ATS specialist.

Compare the attached CV with this job description:

{job_description}

Provide:

1. CV-to-job match score out of 100
2. Matching skills and experience
3. Missing keywords
4. Important experience gaps
5. Suggested CV improvements
6. Whether the candidate should apply
7. Five likely interview questions

Do not invent experience, skills or qualifications.
""",
            "CV Improvement Suggestions": """
You are an expert UK CV writer.

Review the attached CV and provide:

1. Problems reducing interview chances
2. A stronger professional summary
3. Improved achievement-focused bullet-point examples
4. Missing technical and transferable skills
5. Recommended section order
6. Ten practical improvements

Do not invent experience, skills or qualifications.
""",
            "Interview Questions": """
Act as a UK hiring manager.

Based only on the attached CV, generate:

1. Ten likely interview questions
2. Five technical questions
3. Five behavioural questions
4. What a strong answer should include for each category

Do not invent facts not found in the CV.
""",
        }

        with st.spinner("Gemini is analysing your resume..."):
            temp_path = None
            gemini_file = None

            try:
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf",
                ) as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_path = temp_file.name

                gemini_file = client.files.upload(file=temp_path)

                response = None

                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.5-flash",
                            contents=[
                                gemini_file,
                                prompts[analysis_mode],
                            ],
                        )
                        break
                    except Exception:
                        if attempt == 2:
                            raise
                        time.sleep(3)

                st.subheader(analysis_mode)
                st.markdown(response.text)

                st.download_button(
                    label="Download Report",
                    data=response.text,
                    file_name="ai_resume_report.txt",
                    mime="text/plain",
                )

            except Exception as error:
                error_message = str(error)

                if "503" in error_message or "UNAVAILABLE" in error_message:
                    st.warning(
                        "Gemini is temporarily busy. "
                        "Please wait a moment and try again."
                    )
                elif (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                ):
                    st.warning(
                        "The API usage limit has been reached. "
                        "Please wait and try again later."
                    )
                else:
                    st.error(
                        "The analysis could not be completed. "
                        "Please check your connection and try again."
                    )

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

                if gemini_file:
                    try:
                        client.files.delete(name=gemini_file.name)
                    except Exception:
                        pass
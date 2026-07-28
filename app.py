import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

st.title("📄 AI Resume Assistant")
st.write("Upload your CV and compare it with a job description.")

if not api_key:
    st.error("API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"],
)

job_description = st.text_area(
    "Paste the job description",
    height=200,
    placeholder="Paste the full job description here...",
)

if uploaded_file:
    st.success("Resume uploaded successfully!")

    if st.button("Analyse Resume"):
        if not job_description.strip():
            st.warning("Please paste a job description first.")
            st.stop()

        with st.spinner("Gemini is analysing your resume..."):
            temp_path = None

            try:
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf",
                ) as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_path = temp_file.name

                gemini_file = client.files.upload(file=temp_path)

                prompt = f"""
You are an expert UK recruitment consultant and ATS specialist.

Analyse the attached CV and compare it with this job description:

{job_description}

Provide:

1. CV-to-job match score out of 100
2. Matching skills and experience
3. Missing keywords
4. Important experience gaps
5. Suggested CV improvements
6. Whether the candidate should apply
7. Five likely interview questions

Do not invent any experience, skills or qualifications.
Be practical, clear and concise.
"""

                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=[gemini_file, prompt],
                )

                st.subheader("CV and Job Match Report")
                st.markdown(response.text)

            except Exception as error:
                st.error(f"Something went wrong: {error}")

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
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
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(
                    circle at top left,
                    rgba(99, 102, 241, 0.10),
                    transparent 32%
                ),
                linear-gradient(
                    180deg,
                    #f8fafc 0%,
                    #ffffff 45%,
                    #f8fafc 100%
                );
        }

        .main .block-container {
            max-width: 1050px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        .hero {
            padding: 2.2rem;
            border-radius: 24px;
            background:
                linear-gradient(
                    135deg,
                    rgba(79, 70, 229, 0.12),
                    rgba(14, 165, 233, 0.08)
                );
            border: 1px solid rgba(99, 102, 241, 0.18);
            box-shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
            margin-bottom: 1.5rem;
        }

        .hero h1 {
            margin: 0;
            font-size: 2.8rem;
            line-height: 1.1;
            color: #0f172a;
        }

        .hero p {
            margin-top: 0.8rem;
            margin-bottom: 0;
            font-size: 1.08rem;
            color: #475569;
            max-width: 760px;
        }

        .feature-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.8rem;
            margin-top: 1.4rem;
        }

        .feature-card {
            padding: 0.9rem 1rem;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.75);
            border: 1px solid #e2e8f0;
            color: #334155;
            font-size: 0.94rem;
            font-weight: 600;
        }

        div[data-testid="stSelectbox"] > div,
        div[data-testid="stTextArea"] > div,
        div[data-testid="stFileUploader"] {
            border-radius: 16px;
        }

        div[data-testid="stFileUploader"] {
            padding: 1rem;
            border: 1px solid #dbeafe;
            background: rgba(248, 250, 252, 0.85);
        }

        div.stButton > button,
        div.stDownloadButton > button {
            border-radius: 12px;
            font-weight: 700;
            padding: 0.65rem 1.25rem;
            border: none;
        }

        div.stButton > button {
            background: linear-gradient(
                135deg,
                #4f46e5,
                #2563eb
            );
            color: white;
        }

        div.stButton > button:hover {
            background: linear-gradient(
                135deg,
                #4338ca,
                #1d4ed8
            );
            color: white;
        }

        div.stDownloadButton > button {
            background: #0f172a;
            color: white;
        }

        div[data-testid="stAlert"] {
            border-radius: 14px;
        }

        @media (max-width: 800px) {
            .hero h1 {
                font-size: 2.15rem;
            }

            .feature-row {
                grid-template-columns: 1fr;
            }

            .main .block-container {
                padding-top: 1rem;
            }
        }
    </style>

    <div class="hero">
        <h1>📄 AI Resume Assistant</h1>
        <p>
            Analyse your CV for the UK job market, compare it with
            job descriptions, discover skill gaps and prepare for interviews.
        </p>

        <div class="feature-row">
            <div class="feature-card">🎯 CV and job matching</div>
            <div class="feature-card">🧠 AI improvement suggestions</div>
            <div class="feature-card">💬 Interview preparation</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not api_key:
    st.error("API key not found. Check your environment settings.")
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
        height=220,
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
Be practical, clear and concise.
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
Be practical, clear and concise.
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
Be practical, clear and concise.
""",
            "Interview Questions": """
Act as a UK hiring manager.

Based only on the attached CV, generate:

1. Ten likely interview questions
2. Five technical questions
3. Five behavioural questions
4. What a strong answer should include for each category

Do not invent facts not found in the CV.
Be practical, clear and concise.
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

                st.divider()
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
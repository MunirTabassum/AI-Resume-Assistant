import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

st.title("📄 AI Resume Assistant")
st.write("Upload your CV and let Gemini analyse it.")

if not api_key:
    st.error("API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:
    st.success("Resume uploaded successfully!")

    if st.button("Analyse Resume"):
        with st.spinner("Gemini is analysing your resume..."):
            temp_path = None

            try:
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_path = temp_file.name

                gemini_file = client.files.upload(file=temp_path)

                prompt = """
Analyse this resume for the UK job market.

Give:
1. A short professional summary
2. Strongest skills
3. Weak areas
4. Five improvements
5. An overall score out of 100

Do not invent any experience or qualifications.
"""

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[gemini_file, prompt]
                )

                st.subheader("Resume Analysis")
                st.markdown(response.text)

            except Exception as error:
                st.error(f"Something went wrong: {error}")

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
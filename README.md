# AI Resume Assistant

An AI-powered web application that analyses PDF resumes for the UK job market using Google Gemini.

## Features

- Upload a resume in PDF format
- Generate a professional summary
- Identify strongest skills
- Highlight weak areas
- Suggest practical improvements
- Give an overall CV score out of 100
- Compare a PDF CV with a job description
- Generate a CV-to-job match score
- Identify matching skills and missing keywords
- Highlight experience gaps
- Suggest targeted CV improvements
- Generate likely interview questions
- Download the cv and job match report as a text file
- Choose between general Cv analysis, job matching, Cv improvements and interview - question generation
- Display a privacy notice before CV upload
- Show an AI-generated feedback disclaimer
- Provide user-friendly messages for temporary Gemini errors and API limits
- Temporarily process uploaded CV files and remove local temporary copies after analysis

## Privacy and Limitations

- Uploaded CVs may contain personal information, so users should avoid including unnecessary sensitive data.
- The application temporarily processes uploaded PDF files and removes its local temporary copy after analysis.
- Files are sent to the Google Gemini API for processing.
- AI-generated feedback is for guidance only and is not an official ATS assessment.
- Match scores and suggestions may vary and should not replace professional recruitment advice.
- The application may occasionally be unavailable because of API demand or usage limits.

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google GenAI SDK
- python-dotenv

## How to Run

1. Install the required packages:

```bash
pip install -r requirements.txt

2. Create a .env file:
GEMINI_API_KEY=your_api_key_here

3. Start the application:
streamlit run app.py

Security

The .env file is excluded from GitHub to protect the Gemini API key.

Author

Munir Tabassum

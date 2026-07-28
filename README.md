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

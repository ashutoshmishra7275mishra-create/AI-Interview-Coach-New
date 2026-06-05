
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_ai_questions(resume_text):

    prompt = f"""
    Analyze this resume and generate 10 interview questions.

    Resume:
    {resume_text}
    """

    response = model.generate_content(prompt)

    return response.text
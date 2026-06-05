from ai_answer import get_ai_answer

def generate_resume_ai_feedback(resume_text):

    prompt = f"""
    Analyze this resume and provide:

    1. Strengths
    2. Weaknesses
    3. Improvement Suggestions

    Resume:

    {resume_text}
    """

    return get_ai_answer(prompt)
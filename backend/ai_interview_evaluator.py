from ai_answer import get_ai_answer

def evaluate_with_ai(question, answer):

    prompt = f"""
    Evaluate this interview answer.

    Question:
    {question}

    Answer:
    {answer}

    Return ONLY in this format:

    Technical Accuracy: X/10
    Communication: X/10
    Confidence: X/10

    Overall Feedback: One short paragraph
    """

    return get_ai_answer(prompt)
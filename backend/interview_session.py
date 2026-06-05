QUESTIONS = [
    "What are React Hooks?",
    "Explain OOPS concepts.",
    "What is DBMS?",
    "Difference between SQL and MongoDB?",
    "What is a REST API?"
]


def get_question(index):

    if index < len(QUESTIONS):
        return QUESTIONS[index]

    return None


def total_questions():

    return len(QUESTIONS)
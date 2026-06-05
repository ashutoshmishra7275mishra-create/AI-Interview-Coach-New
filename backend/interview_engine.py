def extract_skills(text):

    skills_db = [
        "Python","Java","JavaScript","C++",
        "React","MERN","MongoDB","MySQL",
        "HTML","CSS","Tailwind","NumPy",
        "Pandas","Git","GitHub","Postman",
        "DBMS","OOPS"
    ]

    found = []

    for skill in skills_db:
        if skill.lower() in text.lower():
            found.append(skill)

    return found


def generate_questions(skills):

    questions = []

    question_bank = {
        "Python": "What are Python decorators?",
        "Java": "Explain JVM, JRE and JDK.",
        "JavaScript": "What is event bubbling?",
        "React": "What are React Hooks?",
        "MongoDB": "Difference between SQL and MongoDB?",
        "MySQL": "Explain normalization.",
        "DBMS": "What is ACID property?",
        "OOPS": "Explain inheritance and polymorphism.",
        "Git": "Difference between merge and rebase?",
        "C++": "Difference between pointer and reference?"
    }

    for skill in skills:
        if skill in question_bank:
            questions.append(question_bank[skill])

    return questions

def generate_hr_questions():

    return [
        "Tell me about yourself.",
        "Why should we hire you?",
        "What are your strengths?",
        "What are your weaknesses?",
        "Where do you see yourself in 5 years?",
        "Why do you want to join our company?",
        "Describe a challenging project you worked on.",
        "How do you handle pressure and deadlines?",
        "What motivates you?",
        "Do you have any questions for us?"
    ]
def resume_score(skills):

    score = 0

    score += min(len(skills) * 5, 50)

    if "Python" in skills:
        score += 10

    if "Java" in skills:
        score += 10

    if "React" in skills:
        score += 10

    if "MongoDB" in skills:
        score += 10

    if "Git" in skills:
        score += 10

    return min(score, 100)


def generate_feedback(skills, score):

    strengths = []
    improvements = []

    if "Python" in skills:
        strengths.append("Strong Python programming skills")

    if "Java" in skills:
        strengths.append("Good Object Oriented Programming knowledge")

    if "React" in skills:
        strengths.append("Frontend development experience")

    if score >= 80:
        improvements.append("Practice advanced DSA problems")
        improvements.append("Prepare System Design concepts")
        improvements.append("Work on scalable projects")

    return strengths, improvements
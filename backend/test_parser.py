from interview_engine import generate_hr_questions
from report_generator import generate_report
from resume_parser import extract_text
from interview_engine import extract_skills, generate_questions
from feedback_engine import resume_score, generate_feedback

text = extract_text("../uploads/Ashutosh_resume (1) (2).pdf")

skills = extract_skills(text)

questions = generate_questions(skills)

score = resume_score(skills)

strengths, improvements = generate_feedback(skills, score)

print("\nDetected Skills:")
print(skills)

print("\nResume Score:")
print(score, "/100")

print("\nInterview Questions:\n")

for i, q in enumerate(questions, start=1):
    print(f"{i}. {q}")

print("\nStrengths:")
for s in strengths:
    print("-", s)

print("\nImprovements:")
for i in improvements:
    print("-", i)
    
generate_report(
    score,
    skills,
    questions,
    strengths,
    improvements
)

print("\nPDF Report Generated Successfully")    

hr_questions = generate_hr_questions()

print("\nHR Interview Questions:\n")

for i, q in enumerate(hr_questions, start=1):
    print(f"{i}. {q}")
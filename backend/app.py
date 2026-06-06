
from flask import Flask, request, send_file
import os
import re
from resume_parser import extract_text
from interview_engine import (
    extract_skills,
    generate_questions,
    generate_hr_questions
)
from feedback_engine import (
    resume_score,
    generate_feedback
)
from report_generator import generate_report
from interview_report import generate_interview_report
from mock_interview import evaluate_answer
from resume_ai_feedback import generate_resume_ai_feedback
from ai_answer import get_ai_answer

from interview_session import (
    get_question,
    total_questions
)
from ai_interview_evaluator import evaluate_with_ai


app = Flask(__name__)
generated_questions = []

UPLOAD_FOLDER = "../uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return """
    <html>
    <body>

    <h1>🤖 AI Interview Coach</h1>

    <form action="/upload" method="post" enctype="multipart/form-data">

        <input type="file"
               name="resume"
               accept=".pdf"
               required>

        <br><br>

        <button type="submit">
            Upload Resume
        </button>

    </form>

    <br><br>

    <a href="/mock">
        🎤 Start Mock Interview
    </a>
    
    <br><br>

    <a href="/ask-ai">
        🤖 Ask AI Interview Question
    </a>
    </body>
    </html>
    """


@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)
    

    print("\n==============================")
    print("Saved File:", filepath)
    print("==============================\n")

    try:

        text = extract_text(filepath)
        ai_feedback = generate_resume_ai_feedback(text)

        print("\n========== PDF TEXT ==========")
        print(text[:1000])
        print("==============================\n")

    except Exception as e:
        return f"PDF Parsing Error: {e}"

    skills = extract_skills(text)

    print("Detected Skills:", skills)

    questions = generate_questions(skills)
    
    global generated_questions
    generated_questions = questions
    print("Generated Questions:", generated_questions)

    hr_questions = generate_hr_questions()

    score = resume_score(skills)

    print("Resume Score:", score)

    strengths, improvements = generate_feedback(
        skills,
        score
    )

    generate_report(
        score,
        skills,
        questions,
        strengths,
        improvements
    )
    print("generate_report completed")
    print(
    "PDF Exists:",
    os.path.exists(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "reports",
            "interview_report.pdf"
        )
    )
)

    return f"""
    <html>

    <head>

        <title>AI Interview Coach Report</title>

        <style>

            body {{
                background:#0f172a;
                color:white;
                font-family:Arial;
                padding:30px;
            }}

            .card {{
                background:#1e293b;
                padding:20px;
                border-radius:10px;
                margin-bottom:20px;
            }}

            h1,h2,h3 {{
                color:#38bdf8;
            }}

            a {{
                color:#38bdf8;
                text-decoration:none;
                font-size:18px;
                font-weight:bold;
            }}

        </style>

    </head>

    <body>

    <h1>🤖 AI Interview Coach Report</h1>

    <div class="card">
        <h2>Resume Score: {score}/100</h2>
    </div>

    <div class="card">
        <h3>Detected Skills</h3>

        <ul>
        {''.join(f'<li>{s}</li>' for s in skills)}
        </ul>
    </div>

    <div class="card">
        <h3>Strengths</h3>

        <ul>
        {''.join(f'<li>{s}</li>' for s in strengths)}
        </ul>
    </div>

    <div class="card">
        <h3>Improvements</h3>

        <ul>
        {''.join(f'<li>{i}</li>' for i in improvements)}
        </ul>
    </div>

    <div class="card">
        <h3>Technical Questions</h3>

        <ol>
        {''.join(f'<li>{q}</li>' for q in questions)}
        </ol>
    </div>

    <div class="card">
        <h3>HR Questions</h3>

        <ol>
        {''.join(f'<li>{q}</li>' for q in hr_questions)}
        </ol>
    </div>
    
    <div class="card">

        <h3>🤖 AI Resume Feedback</h3>

        <pre>{ai_feedback}</pre>

</div>

    <div class="card">

        <h3>✅ PDF Report Generated Successfully</h3>

        <br>

        <a href="/download_resume">
            📥 Download PDF Report
        </a>

        <br><br>

        <a href="/mock">
            🎤 Start Mock Interview
        </a>

    </div>

    </body>

    </html>
    """

@app.route("/mock")
def mock_page():

    if generated_questions:
        question = generated_questions[0]
    else:
        question = get_question(0)

    return f"""
    <html>
    <body>

    <h1>🎤 Mock Interview</h1>

    <h3>Question 1/{len(generated_questions) if generated_questions else total_questions()}</h3>

    <h3>{question}</h3>

    <form action="/evaluate" method="post">

        <input type="hidden" name="index" value="0">
        <input type="hidden" name="total_score" value="0">

        <textarea
            name="answer"
            rows="8"
            cols="60"
            required>
        </textarea>

        <br><br>

        <button type="submit">
            Next Question
        </button>

    </form>

    </body>
    </html>
    """



@app.route("/evaluate", methods=["POST"])
def evaluate():
    index = int(request.form["index"])
    total_score = int(request.form["total_score"])
    answer = request.form["answer"]
    
    current_question = (
    generated_questions[index]
    if generated_questions
    else get_question(index)
    )

    ai_feedback = evaluate_with_ai(
    current_question,
    answer
    )
    
    all_feedback = request.form.get(
    "all_feedback",
    ""
    )

    all_feedback += f"""
    Question:
    {current_question}

    Answer:
    {answer}

    {ai_feedback}

    ---------------------
    """

    match = re.search(
    r"Technical Accuracy.*?(\d+)/10",
    ai_feedback,
    re.IGNORECASE | re.DOTALL
    )

    if match:
        score = int(match.group(1))
    else:
        score = 0
    

    print("\n===== AI FEEDBACK =====")
    print(ai_feedback)
    print("=======================\n")

    total_score += score

    next_index = index + 1
    question_count = len(generated_questions) if generated_questions else total_questions()

    if next_index < question_count:
        next_question = generated_questions[next_index] if generated_questions else get_question(next_index)
        return f"""
        <html>
        <body>
        <h1>🎤 Mock Interview</h1>
        <h3>Question {next_index + 1}/{question_count}</h3>
        <h3>{next_question}</h3>
        <form action="/evaluate" method="post">
            <input type="hidden" name="index" value="{next_index}">
            <input type="hidden" name="total_score" value="{total_score}">
            
            <textarea
name="all_feedback"
style="display:none;">{all_feedback}</textarea>
            
            <textarea name="answer" rows="8" cols="60" required></textarea>
            <br><br>
            <button type="submit">Next Question</button>
        </form>
        </body>
        </html>
        """

    # Initialize defaults
    strengths = []
    improvements = []

    # Set final strengths and improvements based on score
    if total_score >= 80:
        strengths = ["Excellent Technical Knowledge", "Strong Communication Skills"]
        improvements = ["Keep Practicing Advanced Questions"]
    elif total_score >= 50:
        strengths = ["Good Understanding of Concepts"]
        improvements = ["Provide More Detailed Answers", "Use Real-world Examples"]
    else:
        strengths = ["Attempted All Questions"]
        improvements = ["Improve Technical Concepts", "Practice Mock Interviews", "Give Detailed Explanations"]

    # Generate report
    generate_interview_report(
    f"{total_score}/{question_count*10}",
    all_feedback
)

    return f"""
    <html>
    <body>
    <h1>🎯 Interview Summary</h1>
    <h2>Total Score: {total_score}/{question_count*10}</h2>
    <h3>Strengths:</h3>
    <ul>
        {''.join(f'<li>{s}</li>' for s in strengths)}
    </ul>
    <h3>Areas to Improve:</h3>
    <ul>
        {''.join(f'<li>{i}</li>' for i in improvements)}
    </ul>
    <h3>🤖 Complete AI Evaluation:</h3>
    <pre>{all_feedback}</pre>
    <br>
    <a href="/download_interview">📥 Download Interview Report</a>
    <br><br>
    <a href="/mock">Start Again</a>
    </body>
    </html>
    """

@app.route("/ask-ai")
def ask_ai():

    return """
    <html>
    <body>

    <h1>🤖 Ask AI Interview Question</h1>

    <form action="/ai-answer" method="post">

        <input
            type="text"
            name="question"
            placeholder="Ask any interview question"
            style="width:500px;height:40px;"
            required>

        <br><br>

        <button type="submit">
            Ask AI
        </button>

    </form>

    </body>
    </html>
    """


@app.route("/ai-answer", methods=["POST"])
def ai_answer():

    question = request.form["question"]

    answer = get_ai_answer(question)

    return f"""
    <html>
    <body>

    <h1>🤖 AI Answer</h1>

    <h3>Question:</h3>
    <p>{question}</p>

    <h3>Answer:</h3>
    <pre>{answer}</pre>

    <br><br>

    <a href="/ask-ai">
        Ask Another Question
    </a>

    </body>
    </html>
    """


# @app.route("/download-interview")
# def download_interview():

#     return send_file(
#         "../reports/interview_summary.pdf",
#         as_attachment=True
#     )

# @app.route("/download")
# def download_report():

#     return send_file(
#         "reports/interview_summary.pdf",
#         as_attachment=True
#     )
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


@app.route("/download_resume")
def download_resume():

    return send_file(
        os.path.join(REPORTS_DIR, "interview_report.pdf"),
        as_attachment=True
    )


@app.route("/download_interview")
def download_interview():

    return send_file(
        os.path.join(REPORTS_DIR, "interview_summary.pdf"),
        as_attachment=True
    )
    
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
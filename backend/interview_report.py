from reportlab.pdfgen import canvas
import os

def generate_interview_report(score, feedback):

    os.makedirs("reports", exist_ok=True)

    pdf = canvas.Canvas("reports/interview_summary.pdf")

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 800, "AI Interview Summary")

    # Score
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 760, f"Total Score: {score}")

    # Strengths
    pdf.drawString(120, 720, "Strengths:")
    pdf.drawString(120, 700, "- Good Technical Knowledge")
    pdf.drawString(120, 680, "- Answered Multiple Questions")

    # Improvements
    pdf.drawString(100, 640, "Areas to Improve:")
    pdf.drawString(120, 620, "- Add More Examples")
    pdf.drawString(120, 600, "- Give Detailed Explanations")

    # AI Evaluation
    pdf.drawString(100, 540, "AI Evaluation:")

    y = 520
    pdf.setFont("Helvetica", 10)

    for line in feedback.split("\n"):

        line = line.replace("■", "")

        if not line.strip():
            y -= 10
            continue

        while len(line) > 120:
            pdf.drawString(50, y, line[:120])
            line = line[120:]
            y -= 15

            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = 800

        pdf.drawString(50, y, line)
        y -= 15

        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = 800

    pdf.save()
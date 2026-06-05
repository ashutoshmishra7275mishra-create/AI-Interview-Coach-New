from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(
        score,
        skills,
        questions,
        strengths,
        improvements):

    pdf = SimpleDocTemplate(
        "../reports/interview_report.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Interview Coach Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Resume Score: {score}/100",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Detected Skills:",
            styles["Heading2"]
        )
    )

    for skill in skills:
        content.append(
            Paragraph(
                f"- {skill}",
                styles["BodyText"]
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Strengths:",
            styles["Heading2"]
        )
    )

    for s in strengths:
        content.append(
            Paragraph(
                f"- {s}",
                styles["BodyText"]
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Improvements:",
            styles["Heading2"]
        )
    )

    for i in improvements:
        content.append(
            Paragraph(
                f"- {i}",
                styles["BodyText"]
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Interview Questions:",
            styles["Heading2"]
        )
    )

    for q in questions:
        content.append(
            Paragraph(
                q,
                styles["BodyText"]
            )
        )

    pdf.build(content)
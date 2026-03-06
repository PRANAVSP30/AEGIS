from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_report(customer_name, pan, account, loan_amount, financial, risk):

    filename = f"{customer_name}_loan_report.pdf"

    c = canvas.Canvas(filename, pagesize=letter)

    y = 750

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y, "AGEX Risk Intelligence Report")

    y -= 40

    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Customer Name: {customer_name}")
    y -= 20

    c.drawString(50, y, f"PAN Number: {pan}")
    y -= 20

    c.drawString(50, y, f"Bank Account: {account}")
    y -= 20

    c.drawString(50, y, f"Loan Amount Requested: {loan_amount}")
    y -= 40

    c.drawString(50, y, "Financial Analysis")
    y -= 20

    c.drawString(50, y, f"Detected Income: {financial['income']}")
    y -= 20

    c.drawString(50, y, f"Detected Expenses: {financial['expenses']}")
    y -= 20

    c.drawString(50, y, f"Transactions: {financial['transactions']}")
    y -= 40

    c.drawString(50, y, "Risk Intelligence Scores")
    y -= 20

    c.drawString(50, y, f"Credit Risk: {risk['credit_risk']}")
    y -= 20

    c.drawString(50, y, f"Behaviour Risk: {risk['behaviour_risk']}")
    y -= 20

    c.drawString(50, y, f"Fraud Risk: {risk['fraud_risk']}")
    y -= 20

    c.drawString(50, y, f"Network Risk: {risk['network_risk']}")
    y -= 20

    c.drawString(50, y, f"Final Risk Score: {risk['final_score']}")
    y -= 40

    c.drawString(50, y, "AI Investigation Summary")
    y -= 20

    text = c.beginText(50, y)
    text.textLines(risk["ai_report"])
    c.drawText(text)

    c.save()

    return filename
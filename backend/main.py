from fastapi import FastAPI, UploadFile, File
from backend.risk_engine import calculate_risk
from backend.bank_analyzer import analyze_csv, analyze_pdf
from backend.report_generator import generate_report
import tempfile

app = FastAPI(title="AGEX Risk Intelligence API")


@app.post("/analyze-statement")
async def analyze_statement(file: UploadFile = File(...), loan_amount: float = 0,
                            customer_name: str = "", pan: str = "", account: str = ""):

    filename = file.filename.lower()

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        contents = await file.read()
        temp.write(contents)
        temp_path = temp.name

    if filename.endswith(".csv"):
        financial = analyze_csv(temp_path)

    elif filename.endswith(".pdf"):
        financial = analyze_pdf(temp_path)

    else:
        return {"error": "Unsupported file format"}

    income = financial["income"]
    expenses = financial["expenses"]

    receiver_account = ""

    if len(financial["receivers"]) > 0:
        receiver_account = financial["receivers"][0]

    risk = calculate_risk(income, expenses, loan_amount, receiver_account)

    report_file = generate_report(customer_name, pan, account, loan_amount, financial, risk)

    return {
        "financial_analysis": financial,
        "risk_analysis": risk,
        "report_file": report_file
    }
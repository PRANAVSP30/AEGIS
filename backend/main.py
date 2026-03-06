from fastapi import FastAPI, UploadFile, File
from typing import List
from backend.risk_engine import calculate_risk
from backend.bank_analyzer import analyze_csv, analyze_pdf
from backend.report_generator import generate_report
from backend.fraud_database import init_db
import tempfile

app = FastAPI(title="AGEX Risk Intelligence API")

# Initialize Fraud Intelligence Database
init_db()


@app.post("/analyze-statement")
async def analyze_statement(
    files: List[UploadFile] = File(...),
    loan_amount: float = 0,
    customer_name: str = "",
    pan: str = "",
    account: str = ""
):

    try:

        total_income = 0
        total_expenses = 0
        total_transactions = 0
        all_receivers = []

        for file in files:

            filename = file.filename.lower()

            with tempfile.NamedTemporaryFile(delete=False) as temp:
                contents = await file.read()
                temp.write(contents)
                temp_path = temp.name

            if filename.endswith(".csv"):
                result = analyze_csv(temp_path)

            elif filename.endswith(".pdf"):
                result = analyze_pdf(temp_path)

            else:
                continue

            total_income += result["income"]
            total_expenses += result["expenses"]
            total_transactions += result["transactions"]

            all_receivers.extend(result["receivers"])

        receiver_account = ""

        if len(all_receivers) > 0:
            receiver_account = all_receivers[0]

        financial = {
            "income": total_income,
            "expenses": total_expenses,
            "transactions": total_transactions,
            "receivers": all_receivers
        }

        risk = calculate_risk(
            total_income,
            total_expenses,
            loan_amount,
            receiver_account
        )

        report_file = generate_report(
            customer_name,
            pan,
            account,
            loan_amount,
            financial,
            risk
        )

        return {
            "financial_analysis": financial,
            "risk_analysis": risk,
            "report_file": report_file
        }

    except Exception as e:
        return {"error": str(e)}
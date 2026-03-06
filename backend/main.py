from fastapi import FastAPI, UploadFile, File
from backend.risk_engine import calculate_risk
from backend.bank_analyzer import analyze_csv, analyze_pdf
import tempfile

app = FastAPI(title="AGEX Risk Intelligence API")


@app.post("/analyze-statement")
async def analyze_statement(file: UploadFile = File(...), loan_amount: float = 0):

    try:
        filename = file.filename.lower()

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            contents = await file.read()
            temp.write(contents)
            temp_path = temp.name

        # Detect file type
        if filename.endswith(".csv"):
            result = analyze_csv(temp_path)

        elif filename.endswith(".pdf"):
            result = analyze_pdf(temp_path)

        else:
            return {"error": "Unsupported file format"}

        income = result["income"]
        expenses = result["expenses"]

        receiver_account = ""

        if len(result["receivers"]) > 0:
            receiver_account = result["receivers"][0]

        risk_result = calculate_risk(
            income,
            expenses,
            loan_amount,
            receiver_account
        )

        return {
            "financial_analysis": result,
            "risk_analysis": risk_result
        }

    except Exception as e:
        return {"error": str(e)}
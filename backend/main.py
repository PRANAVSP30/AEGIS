from fastapi import FastAPI
from pydantic import BaseModel
from backend.auth import router as auth_router
from backend.risk_engine import calculate_risk

app = FastAPI(title="AGEX Risk Intelligence API")

app.include_router(auth_router)


class LoanApplication(BaseModel):
    name: str
    income: float
    expenses: float
    loan_amount: float
    receiver_account: str


@app.post("/analyze-loan")
def analyze_loan(data: LoanApplication):

    result = calculate_risk(
        data.income,
        data.expenses,
        data.loan_amount,
        data.receiver_account
    )

    return {
        "customer": data.name,
        "analysis": result
    }
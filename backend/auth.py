from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Example bank employees
employees = {
    "officer1": "bank123",
    "officer2": "secure456"
}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):

    if data.username in employees and employees[data.username] == data.password:
        return {"status": "success", "message": "Login successful"}

    raise HTTPException(status_code=401, detail="Invalid credentials")
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.security import create_dummy_token

router = APIRouter(tags=["Auth"])

# Hardcoded user
VALID_USER = "admin"
VALID_PASS = "password"

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    status: str
    token: str

@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    if req.username == VALID_USER and req.password == VALID_PASS:
        token = create_dummy_token(req.username)
        return {"status": "success", "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

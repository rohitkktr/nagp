from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users = {
    "alice": "password123",
    "bob": "secure456"
}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    if users.get(data.username) == data.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Import necessary modules from FastAPI and Pydantic
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
# Import the function to retrieve user passwords
from users import get_user_password

# Define the FastAPI application instance
app = FastAPI()

# Define the data model for login requests
class LoginRequest(BaseModel):
    username: str
    password: str

# Define the login endpoint
# This endpoint authenticates a user by checking their username and password
@app.post("/login")
def login(data: LoginRequest):
    stored_password = get_user_password(data.username)
    if stored_password and stored_password == data.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

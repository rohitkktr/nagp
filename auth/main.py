# Import necessary modules
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from users import get_user_password

# Define the FastAPI application instance
app = FastAPI()

# ✅ Add CORS middleware to allow requests from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],       # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],       # Allow all headers
)

# Define the data model for login requests
class LoginRequest(BaseModel):
    username: str
    password: str

# Define the login endpoint
@app.post("/login")
def login(data: LoginRequest):
    """
    Authenticate a user by checking their username and password.
    """
    stored_password = get_user_password(data.username)
    if stored_password and stored_password == data.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# ✅ Add health check endpoint
@app.get("/health")
def health_check():
    """
    Simple health check endpoint for ECS/ALB.
    Returns 200 OK if the service is running.
    """
    return {"status": "ok"}

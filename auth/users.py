mock_users = {
    "Rohit": "password123",
    "Admin": "Admin",
}

def get_user_password(username: str) -> str:
    return mock_users.get(username)
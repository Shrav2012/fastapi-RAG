from datetime import datetime, timedelta
from jose import JWTError, jwt

# Demo user storage (in-memory)
users = {
    "testuser": {"username": "testuser", "password": "testpass"}  # plaintext for demo
}

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def authenticate_user(username: str, password: str):
    user = users.get(username)
    if user and user["password"] == password:
        return user
    return None

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

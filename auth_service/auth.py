from jose import jwt

SECRET_KEY = "secret"

def create_token():
    payload = {
        "sub": "12345",
        "level": "admin"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
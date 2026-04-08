from jose import jwt

SECRET_KEY = "secret"

def create_token():
    return jwt.encode({"user": "test"}, SECRET_KEY, algorithm="HS256")
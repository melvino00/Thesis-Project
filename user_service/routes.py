from fastapi import APIRouter, Request, HTTPException
import os
import random
import string
from jose import jwt, JWTError

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

# Payload Generator
def generate_data(count):
    return {"results": [{"id": i, "desc": ''.join(random.choices(string.ascii_letters, k=100))} for i in range(count)]}

PAYLOADS = {
    "small": generate_data(10240),   # Creates 10 KB
    "large": generate_data(102400)   # Creates 100 KB
}

def verify_security(request: Request):
    """Denna funktion SIMULERAR overheaden av Zero Trust"""
    if os.getenv("INTERNAL_SECURITY") == "HTTPS":
        auth_header = request.headers.get("Authorization")
        if not auth_header: raise HTTPException(status_code=401)
        try:
            token = auth_header.split(" ")[1]
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return {"Authorization": auth_header} # Skicka vidare tunga tokenet
        except JWTError: raise HTTPException(status_code=401)
    else:
        # HYBRID
        return {"userLevel": request.headers.get("userLevel", "user")}
    
@router.get("/users/{size}")
async def get_users(size: str, request: Request):

    verify_security(request) 
    return PAYLOADS.get(size, PAYLOADS["small"])
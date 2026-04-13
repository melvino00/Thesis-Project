from fastapi import Request, HTTPException
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        token = auth_header.split(" ")[1]
        # Verify signature and fetch data
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (JWTError, IndexError):
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_headers(request: Request) -> dict:
    """
    Verifies token and returns correct header baseed on environment
    """
    # Always starts with verifying the token
    payload = verify_token(request)
    
    # 2. Build headers by environment
    if os.getenv("INTERNAL_SECURITY") == "HTTPS":
        # Traditionellt: Skicka vidare original-token
        return {"Authorization": request.headers.get("Authorization")}
    else:
        # Simplified header
        return {
            "userID": str(payload.get("sub", "")),
            "userLevel": payload.get("level", "user")
        }
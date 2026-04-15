from fastapi import APIRouter, Request, HTTPException
import httpx, os, random, string
from jose import jwt, JWTError

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

# Payload Generator
def generate_data(count):
    return {"results": [{"id": i, "desc": ''.join(random.choices(string.ascii_letters, k=100))} for i in range(count)]}

PAYLOADS = {"small": generate_data(1000), "medium": generate_data(10000), "large": generate_data(35000)}

def verify_security(request: Request):
    """Simulates overhead of zero trust"""
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

# --- SCENARIO 1: SINGLE HOP ---
@router.get("/single/{size}")
async def get_single(size: str, request: Request):
    verify_security(request) # Validera
    return PAYLOADS.get(size, PAYLOADS["small"]) # Returnera direkt

# --- SCENARIO 2: CHAINED ---
@router.get("/chained/{size}")
async def get_chained(size: str, request: Request):
    forward_headers = verify_security(request) # Validera och hämta headers
    
    # Request is sent further to user_service
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"http://user_service:8000/users/{size}", headers=forward_headers)
        return response.json()
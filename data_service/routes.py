from fastapi import APIRouter, Request, HTTPException
import httpx, os, random, string
from jose import jwt, JWTError

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

# Creates a global client
http_client = httpx.AsyncClient(timeout=30.0)

# Payload Generator
def generate_data(count):
    return {"results": [{"id": i, "desc": ''.join(random.choices(string.ascii_letters, k=100))} for i in range(count)]}

PAYLOADS = {
    "small": generate_data(100),   # Creates ~10 KB
    "large": generate_data(1000)   # Creates ~100 KB
}

def verify_security(request: Request):
    if os.getenv("INTERNAL_SECURITY") == "HTTPS":
        auth_header = request.headers.get("Authorization")
        if not auth_header: raise HTTPException(status_code=401)
        try:
            token = auth_header.split(" ")[1]
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return {"Authorization": auth_header} 
        except JWTError: raise HTTPException(status_code=401)
    else:
        return {"userLevel": request.headers.get("userLevel", "user")}

# --- SCENARIO 1: SINGLE HOP ---
@router.get("/single/{size}")
async def get_single(size: str, request: Request):
    verify_security(request) 
    return PAYLOADS.get(size, PAYLOADS["small"]) 

# --- SCENARIO 2: CHAINED ---
@router.get("/chained/{size}")
async def get_chained(size: str, request: Request):
    forward_headers = verify_security(request) 
    
    response = await http_client.get(f"http://user_service:8000/users/{size}", headers=forward_headers)
    return response.json()
from fastapi import APIRouter, Request, Response
import httpx
import os
from auth import verify_token, get_headers

router = APIRouter()

PROTOCOL = "https" if os.getenv("INTERNAL_SECURITY") == "HTTPS" else "http"
USER_SERVICE_URL = f"{PROTOCOL}://user_service:8000"
DATA_SERVICE_URL = f"{PROTOCOL}://data_service:8000"
AUTH_SERVICE_URL = f"{PROTOCOL}://auth_service:8000"

AUTH_SERVICE_URL = "http://auth_service:8000"

@router.post("/auth")
async def proxy_auth():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{AUTH_SERVICE_URL}/auth")
            response.raise_for_status() # Catches if auth_service is down or returns an error
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Couldn't reach auth_service: {str(e)}")

@router.get("/users")
async def proxy_users(request: Request):
    # Verify and get correct header
    headers = get_headers(request)
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{USER_SERVICE_URL}/users", headers=headers)
    return response.json()

@router.get("/data")
async def proxy_data(request: Request):
    # Verify and get correct header
    headers = get_headers(request)
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{DATA_SERVICE_URL}/data", headers=headers)
    return response.json()
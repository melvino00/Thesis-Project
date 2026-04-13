from fastapi import APIRouter, Request, Response
import httpx
import os
from auth import verify_token, get_headers

router = APIRouter()

PROTOCOL = "https" if os.getenv("INTERNAL_SECURITY") == "HTTPS" else "http"
USER_SERVICE_URL = f"{PROTOCOL}://user_service:8000"
DATA_SERVICE_URL = f"{PROTOCOL}://data_service:8000"
AUTH_SERVICE_URL = f"{PROTOCOL}://auth_service:8000"

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

@router.post("/auth")
async def proxy_auth(request: Request, response: Response):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/auth", json=body)
    return response.json()
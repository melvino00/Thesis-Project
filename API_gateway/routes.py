from fastapi import APIRouter, Request, Response
import httpx
from auth import verify_token

router = APIRouter()

USER_SERVICE_URL = "http://user_service:8000"
DATA_SERVICE_URL = "http://data_service:8000"
AUTH_SERVICE_URL = "http://auth_service:8000"

@router.get("/users")
async def proxy_users(request: Request):
    verify_token(request)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/users")
    return response.json()


@router.get("/data")
async def proxy_data(request: Request):
    verify_token(request)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DATA_SERVICE_URL}/data")
    return response.json()

@router.post("/auth")
async def proxy_auth(request: Request, response: Response):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/auth", json=body)
    return response.json()
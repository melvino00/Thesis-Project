from fastapi import APIRouter, Request
import requests
from auth import verify_token

router = APIRouter()

USER_SERVICE_URL = "http://localhost:8001"
DATA_SERVICE_URL = "http://localhost:8002"


@router.get("/users")
def proxy_users(request: Request):
    verify_token(request)
    response = requests.get(f"{USER_SERVICE_URL}/users")
    return response.json()


@router.get("/data")
def proxy_data(request: Request):
    verify_token(request)
    response = requests.get(f"{DATA_SERVICE_URL}/data")
    return response.json()
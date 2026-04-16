from fastapi import APIRouter, Request, Response, HTTPException
import httpx
import os
from auth import get_headers

router = APIRouter()

AUTH_SERVICE_URL = "http://auth_service:8000"

# Creates a global client
http_client = httpx.AsyncClient(verify=False, timeout=30.0)

@router.post("/auth")
async def proxy_auth():
    try:
        
        response = await http_client.post(f"{AUTH_SERVICE_URL}/auth")
        response.raise_for_status() 
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Couldn't reach auth_service: {str(e)}")

# Single hop
@router.get("/single/{size}")
async def proxy_single(size: str, request: Request):
    headers = get_headers(request)
    
    response = await http_client.get(f"http://data_service:8000/single/{size}", headers=headers)
    return response.json()

# Chained
@router.get("/chained/{size}")
async def proxy_chained(size: str, request: Request):
    headers = get_headers(request)

    response = await http_client.get(f"http://data_service:8000/chained/{size}", headers=headers)
    return response.json()
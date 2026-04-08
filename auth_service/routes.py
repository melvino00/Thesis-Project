from fastapi import APIRouter
from auth import create_token

router = APIRouter()

@router.post("/auth")
def auth():
    return create_token()
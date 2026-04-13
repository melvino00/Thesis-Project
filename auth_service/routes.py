from fastapi import APIRouter
from auth import create_token

router = APIRouter()

#returns a token for testing purposes
#in real environment, this would be a login endpoint that verifies user credentials and returns a token
@router.post("/auth")
def auth():
    return {"token": create_token()}
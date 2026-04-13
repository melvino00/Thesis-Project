from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get("/users")
def get_users():
    userLevel = request.headers.get("userLevel")

    if userLevel == "admin":
        return {"Admin data"}
    
    else:
        return {"users": ["Alice", "Bob", "Charlie"]}
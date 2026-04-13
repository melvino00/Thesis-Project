from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get("/users")
def get_users(request: Request):
    userLevel = request.headers.get("userLevel")

    if userLevel == "admin":
        return {"message": "Admin data"}
    
    else:
        return {"users": ["Alice", "Bob", "Charlie"]}
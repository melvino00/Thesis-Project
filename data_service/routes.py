from fastapi import APIRouter

router = APIRouter()

@router.get("/data")
def get_data():
    return {"value": 123}
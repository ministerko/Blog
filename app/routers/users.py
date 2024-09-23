from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_users():
    return [{"user_id": 1, "username": "user_one"}, {"user_id": 2, "username": "user_two"}]

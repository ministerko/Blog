from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_items():
    return [{"item_id": 1, "name": "Item One"}, {"item_id": 2, "name": "Item Two"}]

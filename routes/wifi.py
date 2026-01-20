from fastapi import APIRouter
from wifi_info import get_wifi_info

router = APIRouter()

@router.get("/wifi")
def wifi_details():
    return get_wifi_info()

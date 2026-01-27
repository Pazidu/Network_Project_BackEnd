from fastapi import APIRouter
from services.deviceHistoryService import update_device_uptime, get_monthly_device_history

router = APIRouter(prefix="/devices/history", tags=["Device History"])

@router.get("/monthly")
def monthly_history():
    return get_monthly_device_history()

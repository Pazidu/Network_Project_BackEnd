from fastapi import APIRouter, Query
from typing import Optional
from services.deviceHistoryService import get_monthly_device_history
from services.wifiUtils import get_current_wifi
from core.database import SessionLocal
from models.WifiNetwork import WifiNetwork

router = APIRouter(prefix="/devices/history", tags=["Device History"])

@router.get("/monthly")
def monthly_history(wifi_id: Optional[int] = Query(None)):
    if wifi_id is None:
        # Try to detect current Wi-Fi
        ssid, bssid = get_current_wifi()
        if not bssid:
            return {"error": "No Wi-Fi detected"}
        # Look up wifi_id in database
        db = SessionLocal()
        wifi = db.query(WifiNetwork).filter_by(bssid=bssid).first()
        db.close()
        if not wifi:
            return {"error": f"Wi-Fi {ssid} not in database"}
        wifi_id = wifi.id

    return get_monthly_device_history(wifi_id)

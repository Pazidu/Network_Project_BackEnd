from fastapi import APIRouter
from core.database import SessionLocal
from models.WifiNetwork import WifiNetwork
from services.wifiUtils import get_current_wifi
from wifi_info import get_wifi_info

router = APIRouter()

@router.get("/wifi")
def wifi_details():
    return get_wifi_info()

@router.get("/wifiid")
def wifi_id():
    ssid, bssid = get_current_wifi()
    if not bssid:
        return {"id": None}

    db = SessionLocal()
    try:
        wifi = db.query(WifiNetwork).filter_by(bssid=bssid).first()
        return {"id": wifi.id if wifi else None}
    finally:
        db.close()

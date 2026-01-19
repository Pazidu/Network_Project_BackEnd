from fastapi import APIRouter
from services.deviceServices import scan_network

router = APIRouter()

@router.get("/getAllDevices")
def get_devices():
    return {
        "count": len(scan_network()),
        "devices": scan_network()
    }
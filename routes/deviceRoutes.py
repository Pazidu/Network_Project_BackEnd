from fastapi import APIRouter, Depends
from services.deviceServices import get_cached_devices
from dependencies.auth import get_current_user

router = APIRouter()


@router.get("/getAllDevices")
def get_devices(current_user=Depends(get_current_user)):
    devices = get_cached_devices()
    return {
        "count": len(devices),
        "devices": devices
    }

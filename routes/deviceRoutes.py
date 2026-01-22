from fastapi import APIRouter, Depends
from services.deviceServices import get_cached_devices, force_scan
from dependencies.auth import get_current_user

router = APIRouter()


@router.get("/getAllDevices")
def get_devices(current_user=Depends(get_current_user)):
    devices = get_cached_devices()
    return {
        "ok": True,
        "devices": devices
    }


@router.post("/refresh")
def refresh_devices(current_user=Depends(get_current_user)):
    force_scan()
    return {"message": "Scan started"}

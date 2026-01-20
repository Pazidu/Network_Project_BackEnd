from fastapi import APIRouter, Depends
from services.deviceServices import scan_network
from dependencies.auth import get_current_user

router = APIRouter()
import subprocess

def scan_network_non_root():
    result = subprocess.run(["arp", "-n"], capture_output=True, text=True)
    devices = scan_network()
    print(devices)
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 3:
            devices.append({
                "ip": parts[0],
                "mac": parts[2],
                "status": "connected"
            })
    return devices
@router.get("/getAllDevices")
def get_devices(current_user=Depends(get_current_user)):
    devices = scan_network_non_root()
    return {
        "count": len(devices),
        "devices": devices
    }

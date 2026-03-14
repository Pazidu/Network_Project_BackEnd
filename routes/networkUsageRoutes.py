from fastapi import APIRouter
from datetime import datetime
import psutil
import socket
import json
import os

from core.database import SessionLocal
from wifi_info import get_wifi_info
from services.deviceServices import device_cache, cache_lock
from models.Sitevisited import WebsiteLog
from sqlalchemy import func

usage_router = APIRouter()

USAGE_FILE = "monthly_baseline.json"


# ===================== helpers =====================
def load_baseline():
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
    return None


def save_baseline(month, sent, recv):
    with open(USAGE_FILE, "w") as f:
        json.dump(
            {
                "month": month,
                "bytes_sent": sent,
                "bytes_recv": recv
            },
            f
        )


def get_ip_mac(interface):
    ip = None
    mac = None
    for addr in psutil.net_if_addrs().get(interface, []):
        if addr.family == socket.AF_INET:
            ip = addr.address
        elif addr.family == psutil.AF_LINK:
            mac = addr.address
    return ip, mac


# ===================== TOTAL NETWORK USAGE (MONTHLY) =====================
@usage_router.get("/totalUsage")
def get_network_usage():
    wifi = get_wifi_info()
    interface = wifi.get("adapter_name")

    if not interface:
        return {"error": "Wi-Fi adapter not found"}

    stats = psutil.net_io_counters(pernic=True).get(interface)
    if not stats:
        return {"error": "Network stats not available"}

    now = datetime.now()
    current_month = now.strftime("%Y-%m")
    baseline = load_baseline()

    if not baseline or baseline["month"] != current_month:
        save_baseline(current_month, stats.bytes_sent, stats.bytes_recv)
        upload = 0
        download = 0
    else:
        upload = max(0, stats.bytes_sent - baseline["bytes_sent"])
        download = max(0, stats.bytes_recv - baseline["bytes_recv"])

    ip, mac = get_ip_mac(interface)

    return {
        "period": f"Since {current_month}-01",
        "interface": interface,
        "ssid": wifi.get("ssid"),
        "signal_strength": wifi.get("signal_strength"),
        "ip": ip,
        "mac": mac,
        "usage": {
            "upload_mb": round(upload / (1024 * 1024), 2),
            "download_mb": round(download / (1024 * 1024), 2)
        }
    }


# ===================== DEVICE-WISE USAGE =====================
@usage_router.get("/deviceUsage")
def get_device_usage():
    devices = []

    with cache_lock:
        for dev in device_cache.values():
            devices.append({
                "device_name": dev.get("device_name", "Unknown"),
                "ip": dev.get("ip"),
                "mac": dev.get("mac"),
                "status": dev.get("status"),
                "upload_mb": round(dev.get("bytes_sent", 0) / (1024 * 1024), 2),
                "download_mb": round(dev.get("bytes_recv", 0) / (1024 * 1024), 2),
                "packets_sent": dev.get("packets_sent", 0),
                "packets_recv": dev.get("packets_recv", 0),
                "session_count": len(dev.get("sessions", {})) 
            })

    return {
        "connected_devices": len(devices),
        "devices": devices
        
    }


# ===================== REAL TIME WIFI INFO =====================
@usage_router.get("/realUsage")
def get_real_network_usage():
    return get_wifi_info()

@usage_router.get("/Sitevisited/{mac}")
def daily_stats(mac: str):
    db = SessionLocal()

    results = (
        db.query(
            func.date(WebsiteLog.timestamp).label("day"),
            func.count(WebsiteLog.id).label("count")
        )
        .filter(WebsiteLog.mac_address == mac)
        .group_by(func.date(WebsiteLog.timestamp))
        .all()
    )

    db.close()

    return [{"date": str(r.day), "count": r.count} for r in results]
from datetime import datetime, date ,timedelta
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.WifiNetwork import WifiNetwork
from models.device_connection_history import DeviceHistory
from sqlalchemy import func
from models.WifiNetwork import WifiNetwork
from services.wifiUtils import get_current_wifi
from models.Notification import Notification
from services.security_engine import calculate_risk

HEARTBEAT_INTERVAL = 5  # default interval


def get_monthly_device_history(id: int):
    db: Session = SessionLocal()
    try:
        since = datetime.utcnow() - timedelta(days=30)
        print(f"Fetching history for Wi-Fi ID: {id}, since: {since.date()}")
        new_threshold = datetime.utcnow() - timedelta(hours=24)

        rows = (
            db.query(
                DeviceHistory.mac_address,
                DeviceHistory.ip_address,
                DeviceHistory.device_name,
                DeviceHistory.risk_score,
                DeviceHistory.risk_level,
                func.sum(DeviceHistory.total_uptime_seconds).label("uptime"),
                func.min(DeviceHistory.first_seen).label("first_seen"),
            )
            .filter(
                DeviceHistory.wifi_id == id,
                DeviceHistory.date >= since.date()
            )
            .group_by(
                DeviceHistory.mac_address,
                DeviceHistory.ip_address,
                DeviceHistory.device_name
            )
            .all()
        )

        return [
            {
                "mac_address": r.mac_address,
                "ip": r.ip_address,
                "device_name": r.device_name,
                "total_uptime_seconds": r.uptime or 0,
                "risk_score": r.risk_score,
                "risk_level": r.risk_level,
                "is_new": r.first_seen >= new_threshold
            }
            for r in rows
        ]
    finally:
        db.close()



def update_device_uptime(ip, mac, name, ssid, bssid):
    db = SessionLocal()

    # 1️⃣ Find or create Wi-Fi
    wifi = db.query(WifiNetwork).filter_by(bssid=bssid).first()
    if not wifi:
        wifi = WifiNetwork(ssid=ssid, bssid=bssid)
        db.add(wifi)
        db.commit()
        db.refresh(wifi)

    # 2️⃣ Update device history
    today = date.today()
    record = db.query(DeviceHistory).filter(
        DeviceHistory.wifi_id == wifi.id,
        DeviceHistory.mac_address == mac,
        DeviceHistory.date == today
    ).first()

    if not record:
        record = DeviceHistory(
            wifi_id=wifi.id,
            ip_address=ip,
            mac_address=mac,
            device_name=name,
            first_seen=datetime.utcnow(),
            last_seen=datetime.utcnow(),
            total_uptime_seconds=HEARTBEAT_INTERVAL,
            date=today
        )
        db.add(record)

        score,level = calculate_risk(record, is_new=True)
        record.risk_score = score
        record.risk_level = level
        notification = Notification(
            title="New Device Connected",
            message=f"Device {name} ({mac}) connected to Wi-Fi {ssid}.",
            type="new_device"
        )
        db.add(notification)
    else:
        record.last_seen = datetime.utcnow()
        record.total_uptime_seconds += HEARTBEAT_INTERVAL

        score,level = calculate_risk(record)
        record.risk_score = score   
        record.risk_level = level

        if level == "Dangerous":
            alert = Notification(
                title="High Risk Device Detected",
                message=f"Device {name} ({mac}) has a risk score of {score} on Wi-Fi {ssid}.",
                type="high_risk"
            )
            db.add(alert)

    db.commit()
    db.close()


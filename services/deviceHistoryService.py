from datetime import datetime, date
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.device_connection_history import DeviceHistory

HEARTBEAT_INTERVAL = 5  # default interval
from datetime import datetime, timedelta
from sqlalchemy import func

def get_monthly_device_history():
    db: Session = SessionLocal()
    try:
        since = datetime.utcnow() - timedelta(days=30)
        new_threshold = datetime.utcnow() - timedelta(hours=24)

        rows = (
            db.query(
                DeviceHistory.ip_address,
                DeviceHistory.device_name,
                DeviceHistory.mac_address,
                func.sum(DeviceHistory.total_uptime_seconds).label("uptime"),
                func.min(DeviceHistory.first_seen).label("first_seen"),
            )
            .filter(DeviceHistory.date >= since.date())
            .group_by(
                DeviceHistory.ip_address,
                DeviceHistory.device_name,
                DeviceHistory.mac_address
            )
            .all()
        )

        result = []
        for r in rows:
            result.append({
                "ip": r.ip_address,
                "device_name": r.device_name,
                "total_uptime_seconds": r.uptime,
                "is_new": r.first_seen >= new_threshold
            })

        return result
    finally:
        db.close()

def update_device_uptime(ip, mac=None, name=None, seconds=HEARTBEAT_INTERVAL):
    db: Session = SessionLocal()
    today = date.today()
    try:
        record = db.query(DeviceHistory).filter(
            DeviceHistory.ip_address == ip,
            DeviceHistory.date == today
        ).first()

        if not record:
            record = DeviceHistory(
                ip_address=ip,
                mac_address=mac,
                device_name=name or "Unknown",
                first_seen=datetime.utcnow(),
                last_seen=datetime.utcnow(),
                total_uptime_seconds=seconds,
                date=today
            )
            db.add(record)
        else:
            record.last_seen = datetime.utcnow()
            record.total_uptime_seconds += seconds

        db.commit()
    finally:
        db.close()


import datetime
from fastapi import APIRouter
from sqlalchemy import func
from core.database import SessionLocal
from models.device_connection_history import DeviceHistory

router = APIRouter(prefix="/security", tags=["Security"])

@router.get("/summary")
def security_summary(wifi_id: int):
    db = SessionLocal()

    dangerous = db.query(DeviceHistory)\
        .filter(DeviceHistory.wifi_id == wifi_id,
                DeviceHistory.risk_level == "Dangerous")\
        .count()

    warning = db.query(DeviceHistory)\
        .filter(DeviceHistory.wifi_id == wifi_id,
                DeviceHistory.risk_level == "Warning")\
        .count()

    safe = db.query(DeviceHistory)\
        .filter(DeviceHistory.wifi_id == wifi_id,
                DeviceHistory.risk_level == "Safe")\
        .count()

    db.close()

    return {
        "dangerous": dangerous,
        "warning": warning,
        "safe": safe
    }

@router.get("/security-graph/{wifi_id}")
def security_graph(wifi_id: int):
    db = SessionLocal()

    result = db.query(
        DeviceHistory.risk_level,
        func.count(DeviceHistory.id)
    ).filter(
        DeviceHistory.wifi_id == wifi_id
    ).group_by(DeviceHistory.risk_level).all()

    db.close()

    return [
        {"risk_level": r[0], "count": r[1]}
        for r in result
    ]

@router.get("/uptime-graph/{wifi_id}")
def uptime_graph(wifi_id: int):
    db = SessionLocal()

    rows = db.query(
        DeviceHistory.date,
        func.sum(DeviceHistory.total_uptime_seconds)
    ).filter(
        DeviceHistory.wifi_id == wifi_id
    ).group_by(DeviceHistory.date)\
     .order_by(DeviceHistory.date)\
     .all()

    db.close()

    return [
        {
            "date": str(r[0]),
            "uptime_hours": round((r[1] or 0) / 3600, 2)
        }
        for r in rows
    ]
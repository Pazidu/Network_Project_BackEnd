# routers/network_usage.py
from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.Sitevisited import WebsiteLog
from datetime import datetime

router = APIRouter(prefix="/network-usage", tags=["Network Usage"])

@router.get("/siteVisits")
def get_site_visits(mac: str = Query(...)):
    db: Session = SessionLocal()
    try:
        records = db.query(WebsiteLog).filter(WebsiteLog.mac == mac).all()
        result = []
        for r in records:
            result.append({
                "domain": r.website,
                "visit_count": r.visits,
                "last_visit": r.last_visit.strftime("%Y-%m-%d %H:%M:%S") if r.last_visit else None
            })
        return {"sites": result}
    finally:
        db.close()
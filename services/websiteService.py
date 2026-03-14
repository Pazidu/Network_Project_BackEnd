from models.Sitevisited import WebsiteLog
from core.database import SessionLocal
from datetime import datetime

def save_dns(mac, domain):
    db = SessionLocal()
    try:
        record = (
            db.query(WebsiteLog)
            .filter_by(mac=mac, website=domain)
            .first()
        )

        if record:
            record.visits += 1
            record.last_visit = datetime.utcnow()
        else:
            record = WebsiteLog(
                mac=mac,
                website=domain,
                visits=1,
                last_visit=datetime.utcnow()
            )
            db.add(record)

        db.commit()

    except Exception as e:
        print("DB ERROR:", e)
        db.rollback()
    finally:
        db.close()
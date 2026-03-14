from fastapi import APIRouter, Depends
from models.Notification import Notification
from sqlalchemy.orm import Session
from core.database import get_db   # 👈 correct

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
def get_notifications(db: Session = Depends(get_db)):   # 👈 correct
    notifications = db.query(Notification)\
        .order_by(Notification.created_at.desc())\
        .all()

    return notifications

@router.get('/unread-count')
def get_unread_count(db: Session = Depends(get_db)):
    unread_count = db.query(Notification)\
        .filter(Notification.is_read == False)\
        .count()
    return {"unread_count": unread_count}

@router.post('/mark-read/{notification_id}')
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        return {"error": "Notification not found"}

    notification.is_read = True
    db.commit()
    return {"message": "Notification marked as read"}
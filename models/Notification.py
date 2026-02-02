from sqlalchemy import Column, Integer, String, DateTime ,Boolean
from datetime import datetime
from core.database import Base

class Notification(Base):
        __tablename__ = "notifications"

        id = Column(Integer, primary_key=True, index=True)
        title = Column(String)
        message = Column(String)
        type = Column(String)  # new_device, offline, wifi
        is_read = Column(Boolean, default=False)
        created_at = Column(DateTime, default=datetime.utcnow)
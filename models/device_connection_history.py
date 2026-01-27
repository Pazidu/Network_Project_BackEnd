from sqlalchemy import Column, Integer, String, DateTime, Date
from core.database import Base
from datetime import datetime

class DeviceHistory(Base):
    __tablename__ = "device_history"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    mac_address = Column(String, nullable=True)
    device_name = Column(String, nullable=True)

    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    total_uptime_seconds = Column(Integer, default=0)
    date = Column(Date, index=True)

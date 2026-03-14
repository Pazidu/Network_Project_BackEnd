from sqlalchemy import Column, Integer, String, DateTime, Date , ForeignKey
from core.database import Base
from datetime import datetime

class DeviceHistory(Base):
    __tablename__ = "device_connection_history"

    id = Column(Integer, primary_key=True)

    wifi_id = Column(Integer, ForeignKey("wifi_networks.id"), index=True)

    ip_address = Column(String, index=True)
    mac_address = Column(String, index=True)
    device_name = Column(String)

    date = Column(Date)
    risk_score = Column(Integer, default=0)
    risk_level = Column(String, default="Safe")
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)
    total_uptime_seconds = Column(Integer, default=0)


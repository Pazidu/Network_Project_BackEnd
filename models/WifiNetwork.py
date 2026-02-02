from sqlalchemy import Column, Integer, String, DateTime, Date
from core.database import Base
from datetime import datetime

class WifiNetwork(Base):
    __tablename__ = "wifi_networks"

    id = Column(Integer, primary_key=True)
    ssid = Column(String, index=True)
    bssid = Column(String, unique=True)  # Router MAC
    location = Column(String, nullable=True)
    first_seen = Column(DateTime, default=datetime.utcnow)

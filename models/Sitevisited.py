from sqlalchemy import Column, Integer, String, DateTime
from core.database import Base
from datetime import datetime

class WebsiteLog(Base):
    __tablename__ = "website_logs"

    id = Column(Integer, primary_key=True)
    mac = Column(String(50), index=True, nullable=False)
    website = Column(String(255), index=True, nullable=False)
    visits = Column(Integer, default=1)
    last_visit = Column(DateTime, default=datetime.utcnow)
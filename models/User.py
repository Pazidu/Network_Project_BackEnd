from sqlalchemy import Column, Integer, String
from core.database import Base
from sqlalchemy import Column, String, Integer, DateTime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

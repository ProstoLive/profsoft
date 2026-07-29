from sqlalchemy import Column, Integer, String, Text, DateTime, func

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True)
    status = Column(String, default="pending")
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

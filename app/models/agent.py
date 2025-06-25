"""Agent model representing the agents table."""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.database.base import Base

class Agent(Base, AsyncAttrs):
    """Agent model representing intelligence agents"""
    
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codename = Column(String(50), nullable=False, unique=True, index=True)
    realname = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)
    missionscompleted = Column(Integer, nullable=False, default=0)
    
    def __repr__(self):
        return f"<Agent(id={self.id}, codename='{self.codename}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert agents to dictionary representation"""
        return {
            "id": self.id,
            "codename": self.codename,
            "realname": self.realname,
            "location": self.location,
            "status:": self.status,
            "missionscompleted": self.missionscompleted
        }
    
from sqlalchemy import Column, Integer, String, DateTime, Float, func
from football_bot.database import Base

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(64), unique=True, nullable=False, index=True)
    home_team = Column(String(128), nullable=False)
    away_team = Column(String(128), nullable=False)
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    status = Column(String(32), default="scheduled")
    league = Column(String(128), nullable=True)
    season = Column(String(16), nullable=True)
    kickoff_time = Column(DateTime(timezone=True), nullable=True)
    minute = Column(Integer, nullable=True)
    home_xg = Column(Float, nullable=True)
    away_xg = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

from sqlalchemy import Column, Integer, String, Float, DateTime, func
from football_bot.database import Base

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    country = Column(String(64), nullable=True)
    league = Column(String(128), nullable=True)
    elo_rating = Column(Float, default=1500.0)
    fifa_ranking = Column(Integer, nullable=True)
    form = Column(String(10), nullable=True)
    goals_scored = Column(Integer, default=0)
    goals_conceded = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

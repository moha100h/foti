from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from football_bot.database import Base

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False, index=True)
    prediction_type = Column(String(64), nullable=False)
    home_win_prob = Column(Float, nullable=True)
    draw_prob = Column(Float, nullable=True)
    away_win_prob = Column(Float, nullable=True)
    confidence = Column(Float, nullable=False)
    risk_level = Column(String(16), default="medium")
    explanation = Column(String(1024), nullable=True)
    status = Column(String(16), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

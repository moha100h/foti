from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, func
from football_bot.database import Base


class Bet(Base):
    __tablename__ = "bets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    home = Column(String(128), nullable=False)
    away = Column(String(128), nullable=False)
    selection = Column(String(16), nullable=False)
    selection_name = Column(String(128), nullable=True)
    odds = Column(Float, nullable=False)
    stake = Column(Float, nullable=False, default=0.0)
    model_prob = Column(Float, nullable=True)
    edge = Column(Float, nullable=True)
    result = Column(String(16), default="pending")
    profit = Column(Float, default=0.0)
    league = Column(String(128), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    settled_at = Column(DateTime(timezone=True), nullable=True)

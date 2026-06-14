from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func
from football_bot.database import Base


class User(Base):
    __tablename__ = "users"

    # telegram_id is the primary key — no separate auto-increment id needed
    telegram_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    first_name = Column(String(64), nullable=False, default="")
    last_name = Column(String(64), nullable=True)
    username = Column(String(64), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

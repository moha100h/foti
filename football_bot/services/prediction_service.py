from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from football_bot.models.prediction import Prediction
from football_bot.config import settings

async def get_high_confidence(db: AsyncSession) -> List[Prediction]:
    r = await db.execute(select(Prediction).where(Prediction.confidence >= 0.75)
                         .where(Prediction.status == "pending").order_by(Prediction.confidence.desc()).limit(10))
    return r.scalars().all()

async def get_medium_confidence(db: AsyncSession) -> List[Prediction]:
    r = await db.execute(select(Prediction).where(Prediction.confidence >= settings.CONFIDENCE_THRESHOLD)
                         .where(Prediction.confidence < 0.75).where(Prediction.status == "pending")
                         .order_by(Prediction.confidence.desc()).limit(10))
    return r.scalars().all()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Dict
from football_bot.models.user import User
from football_bot.models.match import Match
from football_bot.models.prediction import Prediction

async def get_top_scorers(db: AsyncSession) -> List[Dict]:
    return []

async def get_top_assists(db: AsyncSession) -> List[Dict]:
    return []

async def get_league_table(db: AsyncSession) -> List[Dict]:
    return []

async def get_bot_stats(db: AsyncSession) -> Dict:
    users = await db.scalar(select(func.count(User.id)))
    matches = await db.scalar(select(func.count(Match.id)))
    predictions = await db.scalar(select(func.count(Prediction.id)))
    return {"users": users or 0, "matches": matches or 0, "predictions": predictions or 0}

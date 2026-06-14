import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Dict
from football_bot.models.user import User
from football_bot.models.match import Match
from football_bot.models.prediction import Prediction
from loguru import logger

SCORERS_URL = "https://api.football-data.org/v4/competitions/PL/scorers"
TABLE_URL = "https://api.football-data.org/v4/competitions/PL/standings"
HEADERS = {"X-Auth-Token": ""}


async def get_top_scorers(db: AsyncSession) -> List[Dict]:
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(SCORERS_URL, headers=HEADERS) as resp:
                if resp.status == 200:
                    data = await resp.json(content_type=None)
                    scorers = data.get("scorers") or []
                    return [
                        {
                            "name": (s.get("player") or {}).get("name", ""),
                            "team": (s.get("team") or {}).get("shortName") or (s.get("team") or {}).get("name", ""),
                            "goals": s.get("goals", 0),
                            "assists": s.get("assists", 0),
                        }
                        for s in scorers[:10]
                    ]
    except Exception as e:
        logger.error(f"stats scorers error: {e}")
    return []


async def get_league_table(db: AsyncSession) -> List[Dict]:
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(TABLE_URL, headers=HEADERS) as resp:
                if resp.status == 200:
                    data = await resp.json(content_type=None)
                    standings = data.get("standings") or []
                    if standings:
                        table = standings[0].get("table") or []
                        return [
                            {
                                "position": t.get("position"),
                                "team": (t.get("team") or {}).get("shortName", ""),
                                "points": t.get("points", 0),
                                "played": t.get("playedGames", 0),
                                "won": t.get("won", 0),
                                "draw": t.get("draw", 0),
                                "lost": t.get("lost", 0),
                                "gd": t.get("goalDifference", 0),
                            }
                            for t in table
                        ]
    except Exception as e:
        logger.error(f"stats table error: {e}")
    return []


async def get_top_assists(db: AsyncSession) -> List[Dict]:
    return []


async def get_bot_stats(db: AsyncSession) -> Dict:
    users = await db.scalar(select(func.count(User.telegram_id)))
    matches = await db.scalar(select(func.count(Match.id)))
    predictions = await db.scalar(select(func.count(Prediction.id)))
    return {"users": users or 0, "matches": matches or 0, "predictions": predictions or 0}

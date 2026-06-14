import aiohttp
from loguru import logger
from typing import List, Dict

LIVE_URL = "https://www.thesportsdb.com/api/v1/json/3/latestsoccer.php"


async def get_live_matches() -> List[Dict]:
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(LIVE_URL) as resp:
                if resp.status == 200:
                    data = await resp.json(content_type=None)
                    events = data.get("events") or []
                    return [
                        {
                            "home": e.get("strHomeTeam", ""),
                            "away": e.get("strAwayTeam", ""),
                            "home_score": e.get("intHomeScore") or "0",
                            "away_score": e.get("intAwayScore") or "0",
                            "status": e.get("strStatus", ""),
                            "league": e.get("strLeague", ""),
                            "minute": e.get("intProgress", ""),
                        }
                        for e in events
                    ]
    except Exception as e:
        logger.error(f"live_service error: {e}")
    return []

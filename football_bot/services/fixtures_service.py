import aiohttp
from datetime import date, timedelta
from loguru import logger
from typing import List, Dict

BASE = "https://www.thesportsdb.com/api/v1/json/3/eventsday.php"


async def _fetch(target_date: str) -> List[Dict]:
    url = BASE + "?d=" + target_date + "&s=Soccer"
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json(content_type=None)
                    events = data.get("events") or []
                    return [
                        {
                            "home": e.get("strHomeTeam", ""),
                            "away": e.get("strAwayTeam", ""),
                            "time": (e.get("strTime") or "")[:5],
                            "league": e.get("strLeague", ""),
                            "status": e.get("strStatus", "NS"),
                            "date": target_date,
                        }
                        for e in events
                    ]
    except Exception as e:
        logger.error(f"fixtures_service error: {e}")
    return []


async def get_today_fixtures() -> List[Dict]:
    return await _fetch(date.today().strftime("%Y-%m-%d"))


async def get_tomorrow_fixtures() -> List[Dict]:
    return await _fetch((date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))

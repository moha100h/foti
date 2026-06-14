import aiohttp
from datetime import date, timedelta
from loguru import logger
from typing import List, Dict

async def _fetch_fixtures(target_date: str) -> List[Dict]:
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={target_date}&s=Soccer"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return [{"home": e.get("strHomeTeam",""), "away": e.get("strAwayTeam",""),
                             "time": e.get("strTime",""), "league": e.get("strLeague",""),
                             "status": e.get("strStatus","NS")} for e in (data.get("events") or [])]
    except Exception as e:
        logger.error(f"Error fetching fixtures: {e}")
    return []

async def get_today_fixtures() -> List[Dict]:
    return await _fetch_fixtures(date.today().strftime("%Y-%m-%d"))

async def get_tomorrow_fixtures() -> List[Dict]:
    return await _fetch_fixtures((date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))

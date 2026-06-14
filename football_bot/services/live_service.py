import aiohttp
from loguru import logger
from typing import List, Dict

THESPORTSDB_URL = "https://www.thesportsdb.com/api/v1/json/3/latestsoccer.php"

async def get_live_matches() -> List[Dict]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(THESPORTSDB_URL, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return [{"home": e.get("strHomeTeam",""), "away": e.get("strAwayTeam",""),
                             "home_score": e.get("intHomeScore","?"), "away_score": e.get("intAwayScore","?"),
                             "status": e.get("strStatus",""), "league": e.get("strLeague",""),
                             "minute": e.get("intProgress","")} for e in (data.get("events") or [])]
    except Exception as e:
        logger.error(f"Error fetching live matches: {e}")
    return []

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

WC_TEAMS = [
    {"name": "برزیل", "flag": "🇧🇷", "group": "A", "points": 0},
    {"name": "آرژانتین", "flag": "🇦🇷", "group": "A", "points": 0},
    {"name": "فرانسه", "flag": "🇫🇷", "group": "B", "points": 0},
    {"name": "انگلیس", "flag": "🏴", "group": "B", "points": 0},
    {"name": "اسپانیا", "flag": "🇪🇸", "group": "C", "points": 0},
    {"name": "آلمان", "flag": "🇩🇪", "group": "C", "points": 0},
    {"name": "پرتغال", "flag": "🇵🇹", "group": "D", "points": 0},
    {"name": "هلند", "flag": "🇳🇱", "group": "D", "points": 0},
]

async def get_wc_groups(db: AsyncSession) -> List[Dict]:
    groups: Dict[str, List] = {}
    for team in WC_TEAMS:
        g = team["group"]
        if g not in groups:
            groups[g] = []
        groups[g].append(team)
    return [{"name": k, "teams": v} for k, v in sorted(groups.items())]

async def get_wc_fixtures(db: AsyncSession) -> List[Dict]:
    return []

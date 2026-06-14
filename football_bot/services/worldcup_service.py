from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

WC_TEAMS = [
    {"name": "\u0628\u0631\u0632\u06cc\u0644", "flag": "\U0001f1e7\U0001f1f7", "group": "A", "points": 0},
    {"name": "\u0622\u0631\u0698\u0627\u0646\u062a\u06cc\u0646", "flag": "\U0001f1e6\U0001f1f7", "group": "A", "points": 0},
    {"name": "\u0641\u0631\u0627\u0646\u0633\u0647", "flag": "\U0001f1eb\U0001f1f7", "group": "B", "points": 0},
    {"name": "\u0627\u0646\u06af\u0644\u06cc\u0633", "flag": "\U0001f3f4", "group": "B", "points": 0},
    {"name": "\u0627\u0633\u067e\u0627\u0646\u06cc\u0627", "flag": "\U0001f1ea\U0001f1f8", "group": "C", "points": 0},
    {"name": "\u0622\u0644\u0645\u0627\u0646", "flag": "\U0001f1e9\U0001f1ea", "group": "C", "points": 0},
    {"name": "\u067e\u0631\u062a\u063a\u0627\u0644", "flag": "\U0001f1f5\U0001f1f9", "group": "D", "points": 0},
    {"name": "\u0647\u0644\u0646\u062f", "flag": "\U0001f1f3\U0001f1f1", "group": "D", "points": 0},
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

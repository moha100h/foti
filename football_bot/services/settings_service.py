"""Runtime key/value settings in DB (admin-editable). Cached in memory."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from football_bot.models.setting import Setting

_cache: dict = {}

SCHEMA = {
    "FOOTBALL_DATA_TOKEN": ("", "str", "\u06a9\u0644\u06cc\u062f football-data.org"),
    "ODDS_API_KEY": ("", "str", "\u06a9\u0644\u06cc\u062f the-odds-api.com"),
    "HOME_ADV": ("1.35", "float", "\u0636\u0631\u06cc\u0628 \u0645\u06cc\u0632\u0628\u0627\u0646\u06cc"),
    "LEAGUE_AVG": ("1.35", "float", "\u0645\u06cc\u0627\u0646\u06af\u06cc\u0646 \u06af\u0644 \u0644\u06cc\u06af"),
    "DC_RHO": ("-0.08", "float", "\u0636\u0631\u06cc\u0628 Dixon-Coles"),
    "ELO_WEIGHT": ("0.30", "float", "\u0648\u0632\u0646 Elo"),
    "HALF_LIFE_DAYS": ("120", "float", "\u0646\u06cc\u0645\u0647\u200c\u0639\u0645\u0631 \u0641\u0631\u0645 (\u0631\u0648\u0632)"),
    "MIN_EDGE": ("0.05", "float", "\u062d\u062f\u0627\u0642\u0644 Edge"),
    "KELLY_CAP": ("0.25", "float", "\u0633\u0642\u0641 Kelly"),
    "KELLY_MULT": ("0.5", "float", "\u0636\u0631\u06cc\u0628 Kelly"),
    "BANKROLL": ("1000", "float", "\u0628\u0627\u0646\u06a9\u200c\u0631\u0648\u0644"),
}

async def get_setting(db: AsyncSession, key: str, default: Optional[str] = None) -> Optional[str]:
    if key in _cache:
        return _cache[key]
    row = await db.get(Setting, key)
    val = row.value if row else (default if default is not None else SCHEMA.get(key, ("",))[0])
    _cache[key] = val
    return val

async def set_setting(db: AsyncSession, key: str, value: str) -> None:
    row = await db.get(Setting, key)
    if row:
        row.value = value
    else:
        db.add(Setting(key=key, value=value))
    await db.flush()
    _cache[key] = value

def cache_get(key: str, default: Optional[str] = None):
    if key in _cache:
        return _cache[key]
    return default if default is not None else SCHEMA.get(key, ("",))[0]

def cfloat(key: str) -> float:
    try:
        return float(cache_get(key))
    except Exception:
        return float(SCHEMA.get(key, ("0",))[0])

async def warm_cache(db: AsyncSession) -> None:
    res = await db.execute(select(Setting))
    for row in res.scalars().all():
        _cache[row.key] = row.value

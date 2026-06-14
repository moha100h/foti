"""Runtime key/value settings stored in DB (admin-editable, e.g. API tokens)."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from football_bot.models.setting import Setting

_cache: dict = {}


async def get_setting(db: AsyncSession, key: str, default: Optional[str] = None) -> Optional[str]:
    if key in _cache:
        return _cache[key]
    row = await db.get(Setting, key)
    val = row.value if row else default
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


def cache_get(key: str) -> Optional[str]:
    return _cache.get(key)


async def warm_cache(db: AsyncSession) -> None:
    res = await db.execute(select(Setting))
    for row in res.scalars().all():
        _cache[row.key] = row.value

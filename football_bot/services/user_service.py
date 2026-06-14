from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from aiogram.types import User as TgUser
from typing import List, Optional
from football_bot.models.user import User

async def get_or_create_user(db: AsyncSession, tg_user: TgUser) -> User:
    result = await db.execute(select(User).where(User.telegram_id == tg_user.id))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(telegram_id=tg_user.id, first_name=tg_user.first_name or "",
                    last_name=tg_user.last_name, username=tg_user.username)
        db.add(user)
        await db.flush()
    else:
        user.first_name = tg_user.first_name or user.first_name
        user.last_name = tg_user.last_name
        user.username = tg_user.username
    return user

async def add_user_manual(db: AsyncSession, telegram_id: int, first_name: str = "",
                          username: Optional[str] = None) -> User:
    user = await db.get(User, telegram_id)
    if user:
        user.is_active = True
        user.is_banned = False
        await db.flush()
        return user
    user = User(telegram_id=telegram_id, first_name=first_name or str(telegram_id),
                username=username, is_active=True)
    db.add(user)
    await db.flush()
    return user

async def remove_user(db: AsyncSession, telegram_id: int) -> bool:
    user = await db.get(User, telegram_id)
    if not user:
        return False
    user.is_active = False
    user.is_banned = True
    await db.flush()
    return True

async def list_users(db: AsyncSession, limit: int = 30) -> List[User]:
    res = await db.execute(select(User).order_by(User.created_at.desc()).limit(limit))
    return list(res.scalars().all())

async def count_users(db: AsyncSession) -> int:
    return await db.scalar(select(func.count(User.telegram_id))) or 0

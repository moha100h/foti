from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aiogram.types import User as TgUser
from football_bot.models.user import User


async def get_or_create_user(db: AsyncSession, tg_user: TgUser) -> User:
    result = await db.execute(select(User).where(User.telegram_id == tg_user.id))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(
            telegram_id=tg_user.id,
            first_name=tg_user.first_name or "",
            last_name=tg_user.last_name,
            username=tg_user.username,
        )
        db.add(user)
        await db.flush()
    else:
        # Update name/username if changed
        user.first_name = tg_user.first_name or user.first_name
        user.last_name = tg_user.last_name
        user.username = tg_user.username
    return user

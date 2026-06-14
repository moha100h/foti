import time
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from collections import defaultdict
from football_bot.config import settings

_user_timestamps: Dict[int, list] = defaultdict(list)


class RateLimitMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message, data: Dict[str, Any]) -> Any:
        if not hasattr(event, "from_user") or event.from_user is None:
            return await handler(event, data)
        user_id = event.from_user.id
        now = time.time()
        window = settings.RATE_LIMIT_WINDOW
        _user_timestamps[user_id] = [t for t in _user_timestamps[user_id] if now - t < window]
        if len(_user_timestamps[user_id]) >= settings.RATE_LIMIT:
            await event.answer("درخواست‌های شما بیش از حد مجاز است. لطفاً کمی صبر کنید.")
            return
        _user_timestamps[user_id].append(now)
        return await handler(event, data)

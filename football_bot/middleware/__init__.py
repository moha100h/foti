from aiogram import Dispatcher
from .db_middleware import DbSessionMiddleware
from .rate_limit import RateLimitMiddleware


def setup_middlewares(dp: Dispatcher):
    dp.message.middleware(DbSessionMiddleware())
    dp.callback_query.middleware(DbSessionMiddleware())
    dp.message.middleware(RateLimitMiddleware())

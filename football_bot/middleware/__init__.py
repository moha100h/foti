from aiogram import Dispatcher
from .db_middleware import DbSessionMiddleware
from .rate_limit import RateLimitMiddleware


def setup_middlewares(dp: Dispatcher):
    db_mw = DbSessionMiddleware()
    rate_mw = RateLimitMiddleware()

    dp.message.middleware(db_mw)
    dp.callback_query.middleware(db_mw)

    # Rate limit on both message and callback_query
    dp.message.middleware(rate_mw)
    dp.callback_query.middleware(rate_mw)

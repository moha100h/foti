from aiogram import Router
from .start import router as start_router
from .live import router as live_router
from .fixtures import router as fixtures_router
from .predictions import router as predictions_router
from .valuebets import router as valuebets_router
from .worldcup import router as worldcup_router
from .stats import router as stats_router
from .settings import router as settings_router
from .users import router as users_router
from .admin import router as admin_router

router = Router()
for r in (start_router, live_router, fixtures_router, predictions_router, valuebets_router,
          worldcup_router, stats_router, settings_router, users_router, admin_router):
    router.include_router(r)

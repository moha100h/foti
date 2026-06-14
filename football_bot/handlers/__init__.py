from aiogram import Router
from .start import router as start_router
from .live import router as live_router
from .fixtures import router as fixtures_router
from .predictions import router as predictions_router
from .worldcup import router as worldcup_router
from .stats import router as stats_router
from .admin import router as admin_router

router = Router()
router.include_router(start_router)
router.include_router(live_router)
router.include_router(fixtures_router)
router.include_router(predictions_router)
router.include_router(worldcup_router)
router.include_router(stats_router)
router.include_router(admin_router)

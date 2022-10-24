from fastapi import APIRouter
from ui.ui_v1.endpoints.strategy import router as strategy_router
from ui.ui_v1.endpoints.data import router as data_router

ui_router = APIRouter()
ui_router.include_router(strategy_router, prefix="/strategy", tags=["strategy"])
ui_router.include_router(data_router, prefix="/data", tags=["data"])
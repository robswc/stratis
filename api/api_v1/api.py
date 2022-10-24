from fastapi import APIRouter

from api.api_v1.endpoints.data import router as data_router
from api.api_v1.endpoints.strategy import router as strategy_router

api_router = APIRouter()
api_router.include_router(data_router, prefix="/data", tags=["data"])
api_router.include_router(strategy_router, prefix="/strategy", tags=["strategy"])

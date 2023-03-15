from fastapi import APIRouter

from api.api_v1.endpoints import data
from app.api.api_v1.endpoints import strategy

api_router = APIRouter()
api_router.include_router(strategy.router, prefix="/strategy", tags=["strategy"])
api_router.include_router(data.router, prefix="/data", tags=["data"])
from typing import List

from fastapi import APIRouter

from components import Strategy

router = APIRouter()

@router.get("/strategy")
async def list_all_strategies():
    strategies = Strategy.objects.all()
    return [s.as_model() for s in strategies]
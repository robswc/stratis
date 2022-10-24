from fastapi import APIRouter
from pydantic import BaseModel

from components.strategy.strategy import StrategyManager

router = APIRouter()

sm = StrategyManager()


class Parameters(BaseModel):
    """Parameters for the strategy."""
    parameters: dict


@router.post("/orders")
async def get_orders(name: str, parameters: Parameters):
    """Gets the orders for a strategy."""
    strategy = sm.get_strategy(name)
    if strategy:
        strategy.run({})
        strategy.backtest.run()
        return strategy.orders()
    return []

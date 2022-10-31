from fastapi import APIRouter
from pydantic import BaseModel

from components.data.ohlcv import OHLCVManager
from components.strategy.strategy import StrategyManager

router = APIRouter()

sm = StrategyManager()


class Parameters(BaseModel):
    """Parameters for the strategy."""
    parameters: dict


@router.post("/orders")
async def get_orders(name: str, parameters: Parameters):
    """Gets the orders for a strategy."""
    strategy = sm.get_new_strategy(name)
    if strategy:
        strategy.run({})
        strategy.backtest.run()
        return strategy.orders()
    return []


@router.post("/signals", response_model=list)
async def get_signals(strategy: str, dataset: str, parameters: Parameters):
    """Gets the signals for a strategy."""
    strategy = sm.get_new_strategy(strategy)
    data = OHLCVManager().get_dataset(dataset)
    strategy.data = data
    if strategy:
        strategy.run({})
        return [s.dict() for s in strategy.signal_manager.signals]
    return []


@router.post("/backtest", response_model=list)
async def get_signals(strategy: str, dataset: str, parameters: Parameters):
    """Gets the signals for a strategy."""
    strategy = sm.get_new_strategy(strategy)
    data = OHLCVManager().get_dataset(dataset)
    if strategy:
        strategy.run({})
        strategy.backtest.run()
        return strategy.signal_manager.signals
    return []

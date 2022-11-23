import json

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import Response

from components.data.ohlcv import OHLCVManager
from components.strategy.strategy import StrategyManager

router = APIRouter()

sm = StrategyManager()


class Parameters(BaseModel):
    """Parameters for the strategy."""
    parameters: dict


@router.get("")
async def get_all_strategies():
    """Gets all available strategies."""
    return [s.__name__ for s in sm.strategies]


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


class BacktestResponse(BaseModel):
    """Response for the backtest."""
    overview: dict
    properties: dict
    positions: list


@router.post("/backtest", response_model=BacktestResponse)
async def get_signals(strategy: str, dataset: str, parameters: Parameters):
    """Gets the signals for a strategy."""
    strategy = sm.get_new_strategy(strategy)
    data = OHLCVManager().get_dataset(dataset)
    if strategy:
        strategy.run({})
    results = strategy.backtest.results()
    return BacktestResponse(
        overview=results["overview"],
        properties=results["properties"],
        positions=results["positions"],
    )

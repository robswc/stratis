from pathlib import Path
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import Response

from components import Strategy
from components.backtest.backtest import BacktestResult
from components.ohlc import DataAdapter
from components.ohlc.symbol import Symbol

router = APIRouter()

class RunStrategyRequest(BaseModel):
    strategy: str
    adapter: str
    data: str

@router.get("/strategy")
async def list_all_strategies():
    """List all strategies"""
    strategies = Strategy.objects.all()
    return [s.as_model() for s in strategies]

@router.get("/")
async def get_strategy(name: str):
    """Get a strategy by name"""
    try:
        strategy = Strategy.objects.get(name=name)
        return strategy.as_model()
    except ValueError:
        return Response(status_code=404)

@router.post("/", response_model=BacktestResult)
async def run_strategy(request: RunStrategyRequest):
    """Run a strategy with data"""
    name = request.strategy
    data_adapter_name = request.adapter
    data = str(request.data)

    da = DataAdapter.objects.get(name=data_adapter_name)
    strategy = Strategy.objects.get(name=name)

    # start from app root
    app_path = Path(__file__).parent.parent.parent.parent
    data_path = app_path / data

    ohlc = da.get_data(data_path, symbol="AAPL")


    backtest_result = strategy.run(data=ohlc)
    return backtest_result
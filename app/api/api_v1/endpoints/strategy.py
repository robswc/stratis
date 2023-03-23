from pathlib import Path
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import Response

from components import Strategy
from components.backtest.backtest import BacktestResult
from components.ohlc import DataAdapter

router = APIRouter()

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

class RunStrategyResponse(BaseModel):
    backtest: BacktestResult
    plots: List[dict]

class RunStrategyRequest(BaseModel):
    strategy: str
    parameters: dict
    adapter: str
    data: str

@router.post("/", response_model=RunStrategyResponse)
async def run_strategy(request: RunStrategyRequest):
    """Run a strategy with data"""

    # get arguments from request
    name = request.strategy
    data_adapter_name = request.adapter
    data = str(request.data)
    parameters = request.parameters if request.parameters else {}

    # get strategy and data adapter
    try:
        da = DataAdapter.objects.get(name=data_adapter_name)
    except ValueError:
        return Response(status_code=404, content="Data adapter not found")
    try:
        strategy = Strategy.objects.get(name=name)
    except ValueError:
        return Response(status_code=404, content="Strategy not found")

    # start from app root, get data
    app_path = Path(__file__).parent.parent.parent.parent
    data_path = app_path / data
    # if using API adapter
    if da.name == 'APIDataAdapter':
        ohlc = da.get_data(symbol=data)
    else:
        ohlc = da.get_data(data_path, symbol=data)

    backtest_result, plots = strategy.run(data=ohlc, parameters=parameters, plots=True)
    return RunStrategyResponse(backtest=backtest_result, plots=[p.as_dict() for p in plots])

class SignalsRequest(BaseModel):
    signal_type: str
    strategy: RunStrategyRequest

@router.post("/signals")
async def run_signals(request: SignalsRequest):
    """Run signals"""
    print(request.signal_type)
    pass
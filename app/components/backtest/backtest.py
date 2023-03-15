from typing import Optional, List

from pydantic import BaseModel

from components.orders.position import Position


class BacktestResult(BaseModel):
    pnl: float
    wl_ratio: float
    sharpe_ratio: Optional[float]
    max_drawdown: Optional[float]
    max_drawdown_duration: Optional[int]
    trades: int
    winning_trades: int
    losing_trades: int
    positions: List[Position]

class Backtest:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy
        self.result = None

    def test(self):
        self.result = BacktestResult(
            pnl=0,
            wl_ratio=0,
            trades=0,
            winning_trades=0,
            losing_trades=0,
            positions=[],
        )

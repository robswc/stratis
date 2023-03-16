from typing import Optional, List

from loguru import logger
from pydantic import BaseModel

from components.orders.order import Order
from components.orders.position import Position, PositionClosedException


def get_effect(position: Position, order: Order):
    """Get the effect of an order on a position."""
    if position.get_size() > 0:
        if order.side == 'buy':
            return 'increase'
        elif order.side == 'sell':
            return 'decrease'
    elif position.get_size() < 0:
        if order.side == 'buy':
            return 'decrease'
        elif order.side == 'sell':
            return 'increase'
    else:
        return 'increase'

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
    orders: List[Order]

class Backtest:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy
        self.result = None

    def _sort_orders(self, orders: List[Order]):
        return sorted(orders, key=lambda x: x.timestamp)

    def test(self):
        logger.debug(f'Starting backtest for strategy {self.strategy.name}')

        positions = self.strategy.positions.all()
        orders = self.strategy.orders.all()

        for p in positions:
            p.test(ohlc=self.data)
            print(str(p))

        # calculate win/loss ratio
        losing_trades = len([position for position in positions if position.pnl < 0])
        winning_trades = len([position for position in positions if position.pnl > 0])
        wl_ratio = round(winning_trades / losing_trades, 2) if losing_trades > 0 else 0 if winning_trades == 0 else 1

        # create backtest result
        self.result = BacktestResult(
            pnl=sum([position.pnl for position in positions]),
            wl_ratio=wl_ratio,
            trades=0,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            positions=positions,
            orders=self.strategy.orders.all(),
        )

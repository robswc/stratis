from typing import List

from components.orders.order import Order
from components.orders.position import Position


class PositionManager:
    def __init__(self, strategy: 'BaseStrategy'):
        self._strategy = strategy
        self.positions: List[Position] = []

    def open(self, order_type: str, side: str, quantity: int):
        """Opens a new position"""

        # create order
        order = Order(
            type=order_type,
            side=side,
            qty=quantity,
            symbol=self._strategy.symbol.symbol,
            filled_avg_price=self._strategy.data.close,
            timestamp=self._strategy.data.timestamp,
        )

        self.positions.append(
            Position(
                orders=[order],
            )
        )

    def close(self):
        """Closes the most recent position"""
        self.positions[-1].add_closing_order(ohlc=self._strategy.data)

    def all(self):
        return self.positions
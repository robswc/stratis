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
            timestamp=self._strategy.data.timestamp,
        )

        self.positions.append(
            Position(
                orders=[order],
            )
        )

    def close(self):
        """Closes the most recent position"""
        self.positions[-1].add_closing_order()

    def all(self):
        return self.positions
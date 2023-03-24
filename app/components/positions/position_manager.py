from typing import List

from components.orders.order import Order
from components.positions.position import Position
from components.positions.utils import add_closing_order_to_position

from loguru import logger


class PositionManager:
    def __init__(self, strategy: 'BaseStrategy'):
        self._strategy = strategy
        self.positions: List[Position] = []

    def add(self, position: Position):
        """Adds a position to the manager"""
        # TODO: add validation
        self.positions.append(position)

    def open(self, order_type: str, side: str, quantity: int):
        """Opens a new position"""

        # get the timestamp (it's offset by 1 because we're using the previous close)
        timestamp = self._strategy.data.get_timestamp(offset=1)

        # create order
        order = Order(
            type=order_type,
            side=side,
            qty=quantity,
            symbol=self._strategy.symbol.symbol,
            filled_avg_price=self._strategy.data.close,
            timestamp=timestamp
        )

        self.positions.append(
            Position(
                orders=[order],
            )
        )

    def close(self):
        """Closes the most recent position"""
        try:
            position_to_close = self.positions[-1]
            add_closing_order_to_position(position=position_to_close, ohlc=self._strategy.data)
        except IndexError:
            logger.error(f'{self._strategy} has no positions to close')

    def all(self):
        return self.positions

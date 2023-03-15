from typing import Optional

from pydantic import BaseModel

from components.orders.order import Order


class PositionValidationException(Exception):
    pass

class Position(BaseModel):
    root_order: Order
    closed: bool = False

class BracketPosition(BaseModel):
    take_profit: Optional[Order]
    stop_loss: Optional[Order]

    # def validate(self, **kwargs):
    #     super().validate(**kwargs)
    #     # ensure that both take_profit and stop_loss are not None
    #     if self.take_profit is None and self.stop_loss is None:
    #         raise PositionValidationException('Both take_profit and stop_loss cannot be None.')
    #     # ensure that all orders are of the same symbol
    #     if self.take_profit.symbol != self.stop_loss.symbol:
    #         raise PositionValidationException('All orders must be of the same symbol.')
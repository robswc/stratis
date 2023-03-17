from typing import Optional

from pydantic import BaseModel


class Signal(BaseModel):
    order_type: Optional[str] = None
    side: Optional[str] = None
    quantity: Optional[int] = None
    # symbol: Optional[str] = None
    price: Optional[float] = None

    def from_position(self, position: 'Position'):
        self.order_type = position.orders[0].type
        self.side = 'sell' if position.side == 'sell' else 'buy'
        self.quantity = position.orders[0].qty
        self.price = position.average_entry_price
        return self



class BracketSignal(Signal):
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

    def from_position(self, position: 'Position'):
        super().from_position(position)
        # TODO: add validation for these
        self.stop_loss = [o for o in position.orders if o.type == 'stop'][0].price
        self.take_profit = [o for o in position.orders if o.type == 'limit'][0].price
        return self
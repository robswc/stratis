import datetime
import hashlib
from enum import Enum
from typing import Optional

from pydantic import BaseModel

"""
Similar to Alpaca-py
"""

class OrderValidationError(Exception):
    pass

class TimeInForce(str, Enum):
    DAY = "day"
    GTC = "gtc"
    OPG = "opg"
    CLS = "cls"
    IOC = "ioc"
    FOK = "fok"

class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"

class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"

class Order(BaseModel):
    id: Optional[str]
    timestamp: Optional[int]
    symbol: str
    qty: Optional[float]
    notional: Optional[float]
    side: OrderSide
    type: OrderType
    time_in_force: TimeInForce = TimeInForce.GTC
    extended_hours: Optional[bool]
    client_order_id: Optional[str]
    filled_avg_price: Optional[float]
    # take_profit: Optional[TakeProfitRequest]
    # stop_loss: Optional[StopLossRequest]

    @staticmethod
    def create_market_order(symbol: str, qty: float, side: OrderSide):
        return Order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=OrderType.MARKET,
        )

    def __str__(self):
        dt = datetime.datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return f'{self.type} {self.side} {self.qty} {self.symbol} @ {self.filled_avg_price} ({dt})'

    def __hash__(self):
        h = hashlib.sha256(f'{self.timestamp}{self.symbol}{self.qty}{self.side}{self.type}'.encode())
        return int(h.hexdigest(), 16)

    def get_id(self):
        return hashlib.md5(str(hash(self)).encode()).hexdigest()

    class Config:
        schema_extra = {
            "example": {
                "id": "b6b6b6b6-b6b6-b6b6-b6b6-b6b6b6b6b6b6",
                "symbol": "AAPL",
                "qty": 100,
                "side": "buy",
                "type": "market",
            }
        }

    def __init__(self, **data):
        super().__init__(**data)
        if self.qty is None and self.notional is None:
            raise OrderValidationError("Either qty or notional must be specified.")
        if self.qty is not None and self.notional is not None:
            raise OrderValidationError("Only one of qty or notional can be specified.")
        if self.qty is not None and self.qty <= 0:
            raise OrderValidationError("qty must be greater than 0.")
        if self.notional is not None and self.notional <= 0:
            raise OrderValidationError("notional must be greater than 0.")

        # if valid, set id
        self.id = self.get_id()

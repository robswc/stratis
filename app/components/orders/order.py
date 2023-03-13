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
    symbol: str
    qty: Optional[float]
    notional: Optional[float]
    side: OrderSide
    type: OrderType
    time_in_force: TimeInForce = TimeInForce.GTC
    extended_hours: Optional[bool]
    client_order_id: Optional[str]
    # take_profit: Optional[TakeProfitRequest]
    # stop_loss: Optional[StopLossRequest]

    class Config:
        schema_extra = {
            "example": {
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

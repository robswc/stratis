import datetime
import hashlib
from enum import Enum
from typing import Optional, Union

from loguru import logger
from pydantic import BaseModel, ValidationError, validator

"""
Similar to Alpaca-py
"""


class OrderValidationError(Exception):
    pass


def abbr_type(order_type):
    if order_type == OrderType.MARKET:
        return "mkt"
    elif order_type == OrderType.LIMIT:
        return "lmt"
    elif order_type == OrderType.STOP:
        return "stp"


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
    timestamp: Union[int, None]
    symbol: str
    qty: int
    notional: Optional[float]
    side: OrderSide
    type: Optional[OrderType]
    time_in_force: TimeInForce = TimeInForce.GTC
    extended_hours: Optional[bool]
    client_order_id: Optional[str]
    filled_avg_price: Optional[float]
    filled_timestamp: Optional[int]

    @staticmethod
    def create_market_order(symbol: str, qty: float, side: OrderSide):
        return Order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=OrderType.MARKET,
        )

    def _timestamp_to_datetime(self, timestamp: int):
        if timestamp is not None:
            return datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return 'TBD'

    def __str__(self):
        order_type = abbr_type(self.type).upper()
        side = self.side.upper()
        return f'{order_type} {side} [{self.qty}] {self.symbol} @ {self.filled_avg_price}\t({self._timestamp_to_datetime(self.timestamp)})'

    def __hash__(self):
        h = hashlib.sha256(f'{self.timestamp}{self.symbol}{self.qty}{self.side}{self.type}'.encode())
        return int(h.hexdigest(), 16)

    def get_id(self):
        return hashlib.md5(str(hash(self)).encode()).hexdigest()

    # will eventually make this a proper attribute
    @property
    def price(self):
        return self.filled_avg_price

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
        try:
            super().__init__(**data)
        except ValidationError as e:
            logger.error(e)
            raise e

        # if valid, set id
        self.id = self.get_id()
        self.type = self.type or OrderType.MARKET

        # if side is sell, qty must be negative
        if self.side == OrderSide.SELL:
            self.qty = -abs(self.qty)

    @validator('qty')
    def qty_must_be_int(cls, v):
        assert v != 0, 'qty cannot be 0'
        return v


class LimitOrder(Order):
    limit_price: float

    class Config:
        schema_extra = {
            "example": {
                "id": "b6b6b6b6-b6b6-b6b6-b6b6-b6b6b6b6b6b6",
                "symbol": "AAPL",
                "qty": 100,
                "side": "buy",
                "type": "limit",
                "limit_price": 100.00,
            }
        }

    def __init__(self, **data):
        super().__init__(**data)
        self.type = OrderType.LIMIT

    def __str__(self):
        order_type = abbr_type(self.type).upper()
        side = self.side.upper()
        return f'{order_type} {side} [{self.qty}] {self.symbol} @ {self.limit_price}\t({self._timestamp_to_datetime(self.timestamp)})'


class StopOrder(Order):
    stop_price: float

    class Config:
        schema_extra = {
            "example": {
                "id": "b6b6b6b6-b6b6-b6b6-b6b6-b6b6b6b6b6b6",
                "symbol": "AAPL",
                "qty": 100,
                "side": "buy",
                "type": "stop",
                "stop_price": 100.00,
            }
        }

    def __init__(self, **data):
        super().__init__(**data)
        self.type = OrderType.STOP

    def __str__(self):
        order_type = abbr_type(self.type).upper()
        side = self.side.upper()
        return f'{order_type} {side} [{self.qty}] {self.symbol} @ {self.stop_price}\t({self._timestamp_to_datetime(self.timestamp)})'

from enum import Enum


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

    @staticmethod
    def abbreviation(order_type):
        if order_type == OrderType.MARKET:
            return "mkt"
        elif order_type == OrderType.LIMIT:
            return "lmt"
        elif order_type == OrderType.STOP:
            return "stp"
        elif order_type == OrderType.STOP_LIMIT:
            return "stpl"
        elif order_type == OrderType.TRAILING_STOP:
            return "trsl"


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"

    @staticmethod
    def inverse(side):
        if side == OrderSide.BUY:
            return OrderSide.SELL
        elif side == OrderSide.SELL:
            return OrderSide.BUY

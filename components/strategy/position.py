import datetime
import hashlib


class Order:
    def __init__(
            self,
            order_type: str = 'market',
            side: str = 'none',
            quantity: float = 1,
            price: float = None,
            timestamp: int = None,
            data_index: int = None
    ):
        # create a md5 hash of the order
        self.side = side
        self.order_type = order_type
        self.quantity = quantity
        self.price = price if price is not None else 0
        self.timestamp = datetime.datetime.fromtimestamp(timestamp / 1000) if timestamp else None
        self.data_index = data_index
        self.id = hashlib.md5(self.__repr__().encode('utf-8')).hexdigest()[0:8]
        self.validate()

    def validate(self):
        if self.side.lower() not in ['buy', 'sell']:
            raise Exception(f'Invalid order type {self.order_type}.  Must be buy or sell.')
        if self.order_type.lower() not in ['market', 'limit', 'stop']:
            raise Exception(f'Invalid order type {self.order_type}.  Must be market or limit.')
        if self.quantity <= 0:
            raise Exception(f'Invalid amount {self.quantity}.  Must be greater than 0.')
        if self.order_type != 'market' and self.price <= 0:
            raise Exception(f'Invalid price {self.price}.  Must be greater than 0.')
        if self.timestamp is None:
            raise Exception(f'Invalid timestamp {self.timestamp}.  Must be greater than 0.')

    def __repr__(self):
        return f'{self.order_type} {self.side} {self.quantity}{f" @ {self.price}" if self.price else ""} ({self.timestamp})[{self.data_index}]'


class BasePosition:
    pass


class BasicPosition(BasePosition):
    def __init__(
            self, order_type: str, side: str, quantity: float, price: float, take_profit: float = None,
            take_loss: float = None, timestamp: int = None, data_index: int = None
            ):
        self.order_type = order_type
        self.side = side
        self.quantity = quantity
        self.price = price
        self.take_profit = take_profit
        self.take_loss = take_loss
        self.timestamp = timestamp
        self.data_index = data_index
        self.validate()

    def validate(self):
        return True

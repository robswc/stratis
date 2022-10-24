import datetime

from components.strategy.backtest import Backtest
from loguru import logger

import inspect


def get_decorators(method):
    """Gets decorators of a method"""
    decorators = []
    for d in inspect.getmembers(method, inspect.isfunction):
        if d[1].__name__ == 'wrapper':
            # there has _got_ to be a better way to do this
            wrapper = str(d[1]).split(' ')[1].split('.')[0]
            decorators.append(wrapper)
    return decorators


def runner(func):
    """Decorator to run a strategy, iterating over the data and calling the strategy's run method."""
    logger.debug(f'Running {func.__name__}')

    def wrapper(cls, parameters=None):
        if parameters is None:
            parameters = {}
        if parameters is None:
            parameters = {}
        logger.debug(f'Running {cls.name}.{func.__name__} with parameters {parameters}')
        logger.debug(
            f'Running {cls.name}.{func.__name__} with data [sample : {cls.data.validated_data[0]}] (length : {len(cls.data.validated_data)})')

        # TODO: Do all this when strategy is first created, not when it's run
        methods = [method for method in dir(cls) if callable(getattr(cls, method)) and not method.startswith("__")]
        for m in methods:
            if 'before' in get_decorators(getattr(cls, m)):
                logger.debug(f'Running {cls.name}.{m}')
                getattr(cls, m)()

        # ensure there's only one runner method
        runners = [m for m in methods if 'runner' in get_decorators(getattr(cls, m))]
        if len(runners) > 1:
            raise Exception(f'There are multiple runner methods in {cls.name}.  (There can only be one runner method.)')

        # ensure function has parameters
        if parameters is None:
            parameters = {}

        # loop over the data, call the strategy's run method on each candle
        for idx, candle in enumerate(cls.data.validated_data):
            if len(cls.data.validated_data) != idx + 1:
                cls.data.next()
                func(cls, parameters)

        # TODO: Do all this when strategy is first created, not when it's run
        for m in methods:
            if 'after' in get_decorators(getattr(cls, m)):
                logger.debug(f'Running {cls.name}.{m}')
                getattr(cls, m)()

    return wrapper


def after(func):
    """Decorator to run after a strategy has been run."""
    logger.debug(f'Running After for {func.__name__}')

    def wrapper(cls):
        func(cls)

    return wrapper


def before(func):
    """Decorator to run before a strategy has been run."""
    logger.debug(f'Running Before for {func.__name__}')

    def wrapper(cls):
        func(cls)

    return wrapper


class Parameter:
    """Parameter class for strategies."""

    def __init__(self, name, value, min_value=0, max_value=9999, step=1):
        self.name = name
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.step = step


class Plot(list):
    """Plot class for strategies."""

    def __init__(self):
        super().__init__()

    def from_list(self, data):
        """Creates a plot from a list."""
        self.extend(data)
        return self

    @staticmethod
    def _try_round(value, precision=2):
        """Rounds a value if it's a float."""
        if isinstance(value, float):
            return round(value, precision)
        return value

    def replace_none(self, value):
        """Replaces all None values in a plot with a value."""
        self[:] = [value if x is None else x for x in self]

    def round(self, decimals=2):
        """Rounds all values in a plot."""
        self[:] = [self._try_round(x, decimals) for x in self]


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
        self.side = side
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.timestamp = datetime.datetime.fromtimestamp(timestamp / 1000) if timestamp else None
        self.data_index = data_index
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


class OrderManager:
    def __init__(self):
        self.orders = []


class StrategyManager:
    strategies = []

    def get_strategy(self, name: str):
        """Gets a strategy by name."""
        for s in self.strategies:
            if s.name == name:
                return s
        return None


class Strategy:
    data = None
    artifacts = []
    plots = []
    strategy_manager = StrategyManager

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'

    def as_request_model(self):
        return {
            'name': self.name,
            'parameters': {},
        }

    def __init__(self):
        self.order_manager = OrderManager()
        self.backtest = Backtest()
        self.strategy_manager.strategies.append(self)
        self.name = self.__class__.__name__
        logger.debug(f'Initialized {self.name}')

    def create_order(self, order_type, side, quantity, price=None):
        o = Order(order_type, side, quantity, price, timestamp=self.data.datetime(), data_index=self.data.get_index())
        return self.submit_order(o)

    def orders(self):
        return self.order_manager.orders

    def submit_order(self, order):
        self.order_manager.orders.append(order)
        return 0

    def get_idx(self):
        return self.data._idx

    def run(self, parameters):
        raise NotImplementedError

import datetime

from components.strategy.backtest import Backtest
from loguru import logger

import inspect

from components.strategy.parameters import Parameter
from components.strategy.position import Order, BasicPosition
from components.strategy.signal import SignalManager


def get_decorators(method):
    """Gets decorators of a method"""
    decorators = []
    for d in inspect.getmembers(method, inspect.isfunction):
        if d[1].__name__ == 'wrapper':
            # there has _got_ to be a better way to do this
            wrapper = str(d[1]).split(' ')[1].split('.')[0]
            decorators.append(wrapper)
    return decorators


def get_parameters_from_strategy(cls):
    """Gets parameters from a strategy."""
    logger.debug(f'Getting parameters from {cls.name}')
    parameters = [attr for attr in dir(cls) if type(getattr(cls, attr)) == Parameter]
    return {str(p): getattr(cls, p) for p in parameters}


def add_parameters_to_strategy(cls, parameters):
    """Adds parameters to a strategy."""
    logger.debug(f'Adding parameters to {cls.name}')
    cls.parameters = list(parameters.values())


def runner(func):
    """Decorator to run a strategy, iterating over the data and calling the strategy's run method."""
    logger.debug(f'Running {func.__name__}')

    def wrapper(cls, parameters=None):

        # ensure strategy has data to run on
        if not cls.data:
            raise Exception('No data found for strategy.')

        # get strategy parameters
        parameter_set = get_parameters_from_strategy(cls)
        add_parameters_to_strategy(cls, parameter_set)

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

        # reset the index of the data
        cls.data.reset()

        # set plots
        cls.set_plots()

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


class Plot(list):
    """Plot class for strategies."""

    def __init__(self, name=None, color=None, style=None, width=None, dash=None, opacity=None, overlay=True):
        if name is not None:
            self.name = name
        self.overlay = overlay
        self.color = color
        self.style = style
        self.width = width
        self.dash = dash
        self.opacity = opacity
        super().__init__()

    def from_list(self, data):
        """Creates a plot from a list."""
        self.extend(data)
        return self

    def fill_none(self, value):
        """Fills None values in the plot with a value."""
        for idx, val in enumerate(self):
            if val is None:
                self[idx] = value
        return self

    def config(self):
        """Returns the config for the plot."""
        return {
            'name': self.name,
            'overlay': self.overlay,
            'color': self.color,
            'style': self.style,
            'width': self.width,
            'dash': self.dash,
            'opacity': self.opacity,
        }

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


class OrderManager:
    def __init__(self):
        self.orders = []


class PositionManager:
    def __init__(self):
        self.positions = []


class StrategyManager:
    strategies = []

    def get_new_strategy(self, name: str):
        """Gets a strategy by name."""
        for s in self.strategies:
            if s.__name__ == name:
                return s()
        return None


class Strategy:
    data = None
    artifacts = []
    plots = []
    strategy_manager = StrategyManager
    parameters = []

    def __init__(self):
        self.order_manager = OrderManager()
        self.position_manager = PositionManager()
        self.signal_manager = SignalManager()
        self.backtest = Backtest()
        self.strategy_manager.strategies.append(self.__class__)
        self.name = self.__class__.__name__
        logger.debug(f'Initialized {self.name}')

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'

    def as_request_model(self):
        return {
            'name': self.name,
            'parameters': {},
        }

    def create_order(self, order_type, side, quantity, price=None):
        if price is None:
            price = round(self.data[self.data.get_index()]['close'], 2)
        o = Order(order_type, side, quantity, price=price, timestamp=self.data.datetime(),
                  data_index=self.data.get_index())
        return self.submit_order(o)

    def create_basic_position(self, order_type, side, quantity, price=None, take_profit=None, take_loss=None):
        if price is None:
            price = round(self.data[self.data.get_index()]['close'], 2)
        p = BasicPosition(
            order_type=order_type,
            side=side,
            quantity=quantity,
            price=price,
            timestamp=self.data.datetime(),
            data_index=self.data.get_index(),
            take_profit=round(take_profit, 2) if take_profit is not None else None,
            take_loss=round(take_loss, 2) if take_loss is not None else None,
        )
        return self.submit_position(p)

    def orders(self):
        return self.order_manager.orders

    def submit_order(self, order):
        self.order_manager.orders.append(order)
        return 0

    def submit_position(self, position):
        self.position_manager.positions.append(position)
        return 0

    def get_idx(self):
        return self.data._idx

    def set_plots(self):
        plots = []
        for attr in dir(self):
            if isinstance(getattr(self, attr), Plot):
                plot = getattr(self, attr)
                plot.name = attr
                plots.append(plot)
        logger.debug(f'Found ({len(plots)}) plots')
        self.plots = plots

    def plot_config(self):
        return [p.config() for p in self.plots]

    def run(self, parameters):
        raise NotImplementedError

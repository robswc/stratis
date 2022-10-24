import pytest

from components.data.ohlcv import OHLCV
from components.strategy.strategy import Strategy, runner, after, before


class TestStrategy(Strategy):
    data = OHLCV().from_csv('fixtures/ohlc_valid.csv')

    open_data = []
    close_data = []

    first_open = None
    last_close = None

    some_variable = ''

    @before
    def set_some_variable(self):
        self.some_variable = 'some value'

    @runner
    def run(self, parameters):
        self.open_data.append(self.data.open())
        self.close_data.append(self.data.close())

    @after
    def set_variables(self):
        self.first_open = self.open_data[0]
        self.last_close = self.close_data[-1]


def test_run():
    # create strategy
    s = TestStrategy()

    # run strategy, during the run, the data will be iterated.
    # class variables will be set via the after method.
    s.run({})

    # test "before" decorator
    assert s.some_variable == 'some value'

    # ensure the first open is the same as the first close
    assert round(s.first_open) == 257
    assert round(s.last_close) == 234


class MultiRunners(Strategy):
    data = OHLCV().from_csv('fixtures/ohlc_valid.csv')

    @runner
    def run(self, parameters):
        print('I shouldn\'t be called!')

    @runner
    def run_again(self, parameters):
        print('I shouldn\'t be called!')


def test_multiple_runners():
    # create strategy
    s = MultiRunners()

    with pytest.raises(Exception):
        s.run({})
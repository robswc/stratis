from abc import ABC

from components import Parameter
from components import Strategy, on_step
from components.strategy.decorators import before


class SMACrossOver(Strategy):
    sma_fast = Parameter(10)
    sma_slow = Parameter(20)

    @before
    def hello_world(self):
        print('hello world!')

    @on_step
    def check_for_crossover(self):
        print('run!')
        pass
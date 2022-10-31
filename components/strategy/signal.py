import time
from typing import List

from pydantic import BaseModel


class SignalModel(BaseModel):
    """Signal model."""
    name: str
    parameters: dict
    signals: List[dict]


class Signal:
    def __init__(self, side: str, price: float = None, timestamp: int = None, take_profit: float = None, take_loss: float = None):
        self.side = side
        self.price = price
        self.timestamp = timestamp
        self.take_profit = take_profit
        self.take_loss = take_loss

    def dict(self):
        signal_dict = {}
        if self.side:
            signal_dict['side'] = self.side
        if self.price:
            signal_dict['price'] = self.price
        if self.timestamp:
            signal_dict['timestamp'] = self.timestamp
        if self.take_profit:
            signal_dict['take_profit'] = self.take_profit
        if self.take_loss:
            signal_dict['take_loss'] = self.take_loss
        return signal_dict


class SignalManager:
    def __init__(self):
        self.signals: List[Signal] = []

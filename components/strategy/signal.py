from typing import List

from pydantic import BaseModel


class SignalModel(BaseModel):
    """Signal model."""
    name: str
    parameters: dict
    signals: List[dict]


class Signal:
    def __int__(self):
        pass


class SignalManager:
    def __init__(self):
        self.signals = List[Signal]

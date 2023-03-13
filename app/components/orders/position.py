class PositionValidationException(Exception):
    pass


class Position:
    def __init__(self, side: str, entry_price: float, qty: int):
        self.side: str = side.lower()
        self.entry_price: float = 0.0
        self.qty: int = 0
        self._validate()

    def _validate(self):
        if self.side not in ['long', 'short']:
            raise PositionValidationException(f'{self.side} is an invalid position side. Must be "long" or "short".')
        if self.qty <= 0:
            raise PositionValidationException(f'{self.qty} is an invalid position quantity. Must be greater than 0.')
        if self.entry_price <= 0:
            raise PositionValidationException(f'{self.entry_price} is an invalid position entry price. Must be greater than 0.')

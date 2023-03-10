class Symbol:
    """
    Represents a tradeable instrument.  Feel free to extend this class to fit your needs.
    """

    def __init__(self, symbol: str):
        self.symbol = symbol

    def __str__(self):
        return self.symbol


class Equity(Symbol):
    """
    Represents an equity instrument.
    """

    def __init__(self, symbol: str):
        super().__init__(symbol)
        self.cusip = None
        self.description = ''
        self.exchange = None
        self.type = None

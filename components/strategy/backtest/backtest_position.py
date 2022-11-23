from components.strategy.position import BasicPosition


class BacktestPosition:
    def __init__(self):
        self.entry_price = None
        self.take_profit = None
        self.take_loss = None
        self.side = None
        self.quantity = None
        self.timestamp = None
        self.data_index = None
        self.pnl = None

    def from_position(self, position: BasicPosition) -> 'BacktestPosition':
        """Creates a backtest position from a position object"""
        self.entry_price = position.price
        self.take_profit = position.take_profit
        self.take_loss = position.take_loss
        self.side = position.side
        self.quantity = position.quantity
        self.timestamp = position.timestamp
        self.data_index = position.data_index
        return self

    def test(self, ohlc):
        self.pnl = 10
        print(ohlc)

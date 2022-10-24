from components.strategy.strategy import Strategy


class BasicStrategy(Strategy):
    def __init__(self):
        super().__init__()

    def run(self, parameters):
        print(self.data)
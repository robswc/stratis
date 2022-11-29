from threading import Thread

from components.strategy.backtest.backtest_position import BacktestPosition

from loguru import logger


class BacktestOverview:
    def __init__(self):
        self.net_profit = 0
        self.total_trades = 0
        self.percent_profitable = 0
        self.profit_factor = 0
        self.max_drawdown = 0

    def __str__(self):
        return f'\nNet profit: {self.net_profit}\nTotal trades: {self.total_trades}\nPercent profitable:' \
               f' {self.percent_profitable}\nProfit factor: {self.profit_factor}\nMax drawdown: {self.max_drawdown}\n'

    def as_dict(self):
        return {
            'net_profit': self.net_profit,
            'total_trades': self.total_trades,
            'percent_profitable': self.percent_profitable,
            'profit_factor': self.profit_factor,
            'max_drawdown': self.max_drawdown,
        }


class BacktestProperties:
    def __init__(self):
        self.date_range = None
        self.dataset = None
        self.strategy = None

    def __str__(self):
        return f'Date range: {self.date_range}\nDataset: {self.dataset}\nStrategy: {self.strategy}'

    def as_dict(self):
        return {
            'date_range': self.date_range,
            'dataset': self.dataset,
            'strategy': self.strategy,
        }


class Backtest:
    def __init__(self, strategy):
        self.overview = BacktestOverview()
        self.properties = BacktestProperties()
        self.positions = []
        self.strategy = strategy
        self.threads = []

    def results(self):
        return {
            'overview': self.overview.as_dict(),
            'properties': self.properties.as_dict(),
            'positions': self.positions,
        }

    def run(self):
        logger.info('Running backtest for strategy: {}'.format(self.strategy))
        self.positions = [BacktestPosition().from_position(p) for p in self.strategy.position_manager.positions]
        logger.info(f'Testing ({len(self.positions)}) positions...')

        # create threads for each position
        for idx, position in enumerate(self.positions):
            self.threads.append(Thread(target=position.test, args=(self.strategy.data,)))

        # start threads
        for thread in self.threads:
            thread.start()

        # wait for threads to finish
        for thread in self.threads:
            thread.join()


        # calculate overview
        self.overview.net_profit = sum([p.pnl for p in self.positions])
        self.overview.total_trades = len(self.positions)
        self.overview.percent_profitable = len([p for p in self.positions if p.pnl > 0]) / len(self.positions)
        # self.overview.profit_factor = \
        #     sum([p.pnl for p in self.positions if p.pnl > 0]) / sum([p.pnl for p in self.positions if p.pnl < 0])

        logger.info('[ OK ] Backtest complete')
        logger.info(f'\n{self.overview}')
        return self.results()

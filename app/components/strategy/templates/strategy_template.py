from components import Strategy, on_step, Parameter


class $StrategyName(Strategy):
    """Edit your strategy description here."""

    # my_parameter = Parameter(10) # Example parameter, uncomment to use

    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)
        # add any pre-compiled data here
        # https://github.com/robswc/stratis/wiki/Strategies#init-and-pre-compiled-data-series

    @on_step
    def do_stuff(self):
        print('Running on each step...')
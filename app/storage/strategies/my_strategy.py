from components import Strategy, on_step, Parameter


class MyStrategy(Strategy):
    """Edit your strategy description here."""

    # my_parameter = Parameter(10) # Example parameter, uncomment to use

    @on_step
    def do_stuff(self):
        print('Running on each step...')
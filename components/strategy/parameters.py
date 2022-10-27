class Parameter:
    """Parameter class for strategies."""

    def __init__(self, value, min_value=0, max_value=9999, step=1, alias=None):
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.alias = alias

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __repr__(self):
        return f'Parameter(default={self.value}, min_value={self.min_value}, max_value={self.max_value}, step={self.step}, alias={self.alias})'


class IntegerParameter(Parameter, int):
    """Integer parameter class for strategies."""

    def __int__(self):
        return int(self.value)

    def __repr__(self):
        return f'IntegerParameter(default={self.value}, min_value={self.min_value}, max_value={self.max_value}, step={self.step}, alias={self.alias})'

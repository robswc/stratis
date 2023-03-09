class BaseParameter:
    def __init__(self, name):
        self.name = name
        self._validate()

    def _validate(self):
        raise NotImplementedError

class Parameter:
    def __init__(self, name, value, *args, **kwargs):
        if isinstance(value, bool):
            self.value = BooleanParameter(name, value)
        elif isinstance(value, int):
            self.value = IntegerParameter(name, value, *args, **kwargs)
        elif isinstance(value, float):
            self.value = FloatParameter(name, value, *args, **kwargs)
        else:
            raise ValueError('Invalid parameter type')


class IntegerParameter(BaseParameter):
    def __init__(self, name, value: int, min_value: int, max_value: int):
        self.value = int(value)
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(name)

    def _validate(self):
        if self.value < self.min_value or self.value > self.max_value:
            raise ValueError(f'{self.name} must be between {self.min_value} and {self.max_value}')


class FloatParameter(BaseParameter):
    def __init__(self, name, value: float, min_value: float, max_value: float):
        self.value = float(value)
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(name)

    def _validate(self):
        if self.value < self.min_value or self.value > self.max_value:
            raise ValueError(f'{self.name} must be between {self.min_value} and {self.max_value}')
        # ensure value is a float
        self.value = float(self.value)


class BooleanParameter(BaseParameter):
    def __init__(self, name, value: bool):
        self.value = bool(value)
        super().__init__(name)

    def _validate(self):
        self.value = bool(self.value)



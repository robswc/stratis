class BaseParameter:
    def __init__(self):
        self.name = None
        self._validate()

    def _validate(self):
        raise NotImplementedError

    def __str__(self):
        value = self.__getattribute__('value')
        kwargs = [f'{k}={v}' for k, v in self.__dict__.items() if k != 'name' and k != 'value']
        kwargs_str = '' if len(kwargs) == 0 else f' ({", ".join(kwargs)})'
        return f'{self.name} : {value}{kwargs_str}'


class Parameter:
    def __init__(self, value, *args, **kwargs):
        if isinstance(value, bool):
            self.value = BooleanParameter(value)
        elif isinstance(value, int):
            self.value = IntegerParameter(value, *args, **kwargs)
        elif isinstance(value, float):
            self.value = FloatParameter(value, *args, **kwargs)
        else:
            raise ValueError('Invalid parameter type')

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __bool__(self):
        return bool(self.value)


class IntegerParameter(BaseParameter):
    def __init__(self, value: int, min_value: int = 0, max_value: int = 9999):
        self.value = int(value)
        self.min_value = min_value
        self.max_value = max_value
        super().__init__()

    def __int__(self):
        return self.value

    def _validate(self):
        if self.value < self.min_value or self.value > self.max_value:
            raise ValueError(f'{self} must be between {self.min_value} and {self.max_value}')


class FloatParameter(BaseParameter):
    def __init__(self, value: float, min_value: float, max_value: float):
        self.value = float(value)
        self.min_value = min_value
        self.max_value = max_value
        super().__init__()

    def __float__(self):
        return self.value

    def __int__(self):
        return int(self.value)

    def _validate(self):
        if self.value < self.min_value or self.value > self.max_value:
            raise ValueError(f'{self} must be between {self.min_value} and {self.max_value}')
        # ensure value is a float
        self.value = float(self.value)


class BooleanParameter(BaseParameter):
    def __init__(self, value: bool):
        self.value = bool(value)
        super().__init__()

    def __bool__(self):
        return self.value

    def _validate(self):
        self.value = bool(self.value)

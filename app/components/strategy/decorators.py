import inspect


def extract_decorators(cls):
    befores = []
    steps = []
    afters = []
    methods = [method for method in dir(cls) if callable(getattr(cls, method)) and not method.startswith("__")]
    for method in methods:
        for text, member in inspect.getmembers(getattr(cls, method)):
            if text == '__func__':
                if 'before' in str(member):
                    befores.append(method)
                if 'step' in str(member):
                    steps.append(method)
                if 'after' in str(member):
                    afters.append(method)
    return befores, steps, afters


def on_step(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def before(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def after(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def camel_case(value):
    """Converts a string to camel case."""
    return ''.join(x.capitalize() or '_' for x in value.split('_'))

def snake_case(value):
    """Converts a string to snake case."""
    return ''.join(x.lower() if x.islower() else '_' + x.lower() for x in value)

def pascal_case(value):
    """Converts a string to pascal case."""
    return ''.join(x.capitalize() for x in value.split('_'))

def pascal_to_snake_case(value: str):
    """Converts a string from pascal case to snake case."""
    case = ''
    for i, c in enumerate(value):
        if c.isupper() and i != 0:
            case += '_'
        case += c.lower()
    return case

def kebab_case(value):
    """Converts a string to kebab case."""
    return '-'.join(x.lower() for x in value.split('_'))
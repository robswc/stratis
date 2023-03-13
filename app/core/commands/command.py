from utils.formatting import snake_case, pascal_case


class BaseCommand:

    help = 'Base command'

    def handle(self, *args, **kwargs):
        raise NotImplementedError

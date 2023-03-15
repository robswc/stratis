
class Logic:
    @staticmethod
    def crossover(a: 'Series', b: 'Series') -> bool:
        return a > b and a.shift(1) < b.shift(1)
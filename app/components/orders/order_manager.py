from components.orders.order import Order


class OrderManager:
    def __init__(self):
        self.orders = []

    def add(self, order: Order):
        self.orders.append(order)

    def all(self):
        return self.orders
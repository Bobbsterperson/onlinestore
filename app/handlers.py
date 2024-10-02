
class OrderHandler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, order):
        if self.successor:
            return self.successor.handle(order)

class ValidationHandler(OrderHandler):
    def handle(self, order):
        if not self.validate(order):
            raise Exception("Order validation failed")
        return super().handle(order)

    def validate(self, order):
        return True

class StockUpdateHandler(OrderHandler):
    def handle(self, order):
        self.update_stock(order)
        return super().handle(order)

    def update_stock(self, order):
        pass

class PaymentHandler(OrderHandler):
    def handle(self, order):
        self.process_payment(order)
        return super().handle(order)

    def process_payment(self, order):
        pass

class NotificationHandler(OrderHandler):
    def handle(self, order):
        self.send_notification(order)
        return super().handle(order)

    def send_notification(self, order):
        pass

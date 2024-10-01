from abc import ABC, abstractmethod

class OrderState(ABC):
    @abstractmethod
    def next_state(self, order):
        pass

class ProcessingState(OrderState):
    def next_state(self, order):
        order.status = 'shipped'
        order.save()

class ShippedState(OrderState):
    def next_state(self, order):
        raise Exception("Order is already shipped")

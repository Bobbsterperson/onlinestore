class Command:
    def execute(self):
        pass

class AddToCartCommand(Command):
    def __init__(self, cart, product_id):
        self.cart = cart
        self.product_id = product_id

    def execute(self):
        self.cart.add(self.product_id)

class RemoveFromCartCommand(Command):
    def __init__(self, cart, product_id):
        self.cart = cart
        self.product_id = product_id

    def execute(self):
        self.cart.remove(self.product_id)

class PurchaseCommand(Command):
    def __init__(self, cart, username):
        self.cart = cart
        self.username = username

    def execute(self):
        order = self.cart.create_order(self.username)
        self.cart.items.clear()
        return order

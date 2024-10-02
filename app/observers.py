from .models import Product

class CartObserver:
    def update(self, cart):
        pass

class CartView(CartObserver):
    def update(self, cart):
        for item_id, quantity in cart.items.items():
            product = Product.objects.get(id=item_id)
            print(f"Item: {product.name}, Current Stock: {product.stock}, Quantity in Cart: {quantity}")
        print("Order is about to be processed. Current items in the cart:")
        for item_id, quantity in cart.items.items():
            product = Product.objects.get(id=item_id)
            print(f"Processing Order - Item: {product.name}, Current Stock: {product.stock}, Quantity Ordered: {quantity}")
            new_stock = product.stock - quantity
            print(f"Stock After Shipment: {new_stock}")

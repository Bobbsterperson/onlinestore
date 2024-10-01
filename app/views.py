from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order

class Cart:
    def __init__(self):
        self.items = {}

    def add(self, product_id):
        if product_id in self.items:
            self.items[product_id] += 1
        else:
            self.items[product_id] = 1

    def get_items(self):
        return [{'product': get_object_or_404(Product, id=pid), 'quantity': qty} for pid, qty in self.items.items()]

    def get_total_price(self):
        total = 0
        for pid, qty in self.items.items():
            product = get_object_or_404(Product, id=pid)
            if product.discount:
                discounted_price = product.price - (product.price * product.discount / 100)
            else:
                discounted_price = product.price
            total += discounted_price * qty
        return total

    def create_order(self, user):
        items = self.get_items()
        total_price = self.get_total_price()
        order_items = {item['product'].id: item['quantity'] for item in items}
        order = Order.objects.create(user=user, items=order_items, total_price=total_price)
        return order

cart = Cart()

def store(request):
    products = Product.objects.all()
    cart_items = cart.get_items()
    total_price = cart.get_total_price()
    return render(request, 'store.html', {'products': products, 'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    cart.add(product_id)
    return redirect('store')

def purchase(request):
    if request.method == 'POST':
        username = request.POST.get('username', 'Guest')  # You might have a user session instead
        order = cart.create_order(username)

        # Decrease stock for each item in the order
        for item_id, quantity in order.items.items():
            product = get_object_or_404(Product, id=item_id)
            product.stock -= quantity
            product.save()

        # Clear the cart after purchase
        cart.items.clear()

        return redirect('store')  # Redirect to the store or a confirmation page

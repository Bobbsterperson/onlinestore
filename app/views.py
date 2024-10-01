from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.http import HttpResponse

class Cart:
    def __init__(self):
        self.items = {}

    def add(self, product_id):
        if product_id in self.items:
            self.items[product_id] += 1
        else:
            self.items[product_id] = 1

    def get_items(self):
        return [{'product': get_object_or_404(
            Product, id=pid
            ), 'quantity': qty} for pid,
            qty in self.items.items()]
    
    def get_total_price(self):
        total = 0
        for pid, qty in self.items.items():
            product = get_object_or_404(Product, id=pid)
            total += product.price * qty
        return total
cart = Cart()

def store(request):
    products = Product.objects.all()
    cart_items = cart.get_items()
    total_price = cart.get_total_price()
    return render(request, 'store.html', {'products': products, 'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    cart.add(product_id)
    return redirect('store')

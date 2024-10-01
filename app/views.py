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
        return [{'product': get_object_or_404(Product, id=pid), 'quantity': qty} for pid, qty in self.items.items()]

cart = Cart()

def store(request):
    products = Product.objects.all()
    cart_items = cart.get_items()
    return render(request, 'store.html', {'products': products, 'cart_items': cart_items})

def add_to_cart(request, product_id):
    cart.add(product_id)
    return redirect('store')

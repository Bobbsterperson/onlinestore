from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, cart
from .observers import CartView

cart_view = CartView()
cart.add_observer(cart_view)

def store(request):
    products = Product.objects.all()
    cart_items = cart.get_items()
    total_price = cart.get_total_price()
    return render(request, 'store.html', {'products': products, 'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    cart.add(product_id)
    return redirect('store')

def remove_from_cart(request, product_id):
    cart.remove(product_id)
    return redirect('store')

def purchase(request):
    if request.method == 'POST':
        username = request.POST.get('username', 'Guest')
        order = cart.create_order(username)
        cart.items.clear()
        return redirect('store')

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, cart
from .observers import CartView
from .commands import AddToCartCommand, RemoveFromCartCommand, PurchaseCommand

cart_view = CartView()
cart.add_observer(cart_view)

def store(request):
    products = Product.objects.all()
    cart_items = cart.get_items()
    total_price = cart.get_total_price()
    return render(request, 'store.html', {'products': products, 'cart_items': cart_items, 'total_price': total_price, 'user': request.user})

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            user = User.objects.create_user(username=name)  # Create a user with the name
            login(request, user)  # Log in the newly created user
            messages.success(request, 'Registration successful.')
            return redirect('store')
        else:
            messages.error(request, 'Please provide a name.')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('store')

def add_to_cart(request, product_id):
    command = AddToCartCommand(cart, product_id)
    command.execute()
    return redirect('store')

def remove_from_cart(request, product_id):
    command = RemoveFromCartCommand(cart, product_id)
    command.execute()
    return redirect('store')

def purchase(request):
    if request.method == 'POST':
        username = request.POST.get('username', 'Guest')
        command = PurchaseCommand(cart, username)
        order = command.execute()
        return redirect('store')

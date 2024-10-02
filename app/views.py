# app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, cart
from .observers import CartView
from .commands import AddToCartCommand, RemoveFromCartCommand, PurchaseCommand
from .handlers import ValidationHandler, StockUpdateHandler, PaymentHandler, NotificationHandler

cart_view = CartView()
cart.add_observer(cart_view)

def store(request):
    products = Product.objects.all()
    cart_items = cart.get_items()
    total_price = cart.get_total_price()
    return render(request, 'store.html', {'products': products, 'cart_items': cart_items, 'total_price': total_price})

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
        validation_handler = ValidationHandler()
        stock_update_handler = StockUpdateHandler()
        payment_handler = PaymentHandler()
        notification_handler = NotificationHandler()
        validation_handler.successor = stock_update_handler
        stock_update_handler.successor = payment_handler
        payment_handler.successor = notification_handler
        try:
            validation_handler.handle(order)
        except Exception as e:
            print(f"Order processing failed: {e}")
        return redirect('store')

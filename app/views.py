from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, Item, CartItem, Order

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    else:
        cart = Cart.objects.get(id=cart_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if created:
        cart_item.quantity = 1
    else:
        if cart_item.quantity < item.stock:
            cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_detail')

def cart_detail(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
    else:
        cart = None

    return render(request, 'cart_detail.html', {'cart': cart})

def checkout(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return redirect('store')
    cart = get_object_or_404(Cart, id=cart_id)
    if request.method == 'POST':
        payment_amount = request.POST.get('payment_amount')
        order, created = Order.objects.get_or_create(cart=cart, defaults={'status': 'processing', 'payment_amount': payment_amount})
        if created:
            return redirect('order_detail', order_id=order.id)
        else:
            return render(request, 'checkout.html', {'cart': cart, 'error': 'An order already exists for this cart.'})
    return render(request, 'checkout.html', {'cart': cart})

def store(request):
    items = Item.objects.all()
    return render(request, 'store.html', {'items': items})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

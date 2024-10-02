from django.db import models
from django.shortcuts import get_object_or_404

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
    ]
    user = models.CharField(max_length=100)
    items = models.JSONField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"Order {self.id} by {self.user} - Status: {self.status}"

    def get_item_list(self):
        item_list = []
        for item_id, quantity in self.items.items():
            product = get_object_or_404(Product, id=item_id)
            item_list.append(f"{product.name} (x{quantity})")
        return ", ".join(item_list)
    
    def ship_order(self):
        for item_id, quantity in self.items.items():
            product = get_object_or_404(Product, id=item_id)
            product.stock -= quantity
            product.save()
            cart.notify_observers()

class Cart:
    def __init__(self):
        self.items = {}
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def add(self, product_id):
        if product_id in self.items:
            self.items[product_id] += 1
        else:
            self.items[product_id] = 1
        self.notify_observers()

    def remove(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            self.notify_observers()

    def get_items(self):
        return [{'product': get_object_or_404(Product, id=pid), 'quantity': qty} for pid, qty in self.items.items()]

    def get_total_price(self):
        total = 0
        for pid, qty in self.items.items():
            product = get_object_or_404(Product, id=pid)
            discounted_price = product.price
            if product.discount:
                discounted_price -= discounted_price * (product.discount / 100)
            total += discounted_price * qty
        return total

    def create_order(self, user):
        items = self.get_items()
        total_price = self.get_total_price()
        order_items = {item['product'].id: item['quantity'] for item in items}
        order = Order.objects.create(user=user, items=order_items, total_price=total_price)
        return order

cart = Cart()

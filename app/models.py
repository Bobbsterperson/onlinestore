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
from django.contrib import admin
from .models import Product, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'discount')
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status')
    list_filter = ('status',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)  # Register the Order model

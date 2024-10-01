from django.contrib import admin
from .models import Item, Order, Cart, CartItem

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'image']
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'payment_amount']

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            obj.next_status()
        super().save_model(request, obj, form, change)

admin.site.register(Cart)
admin.site.register(CartItem)

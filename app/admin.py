from django.contrib import admin
from .models import Product, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'discount')
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'get_item_list')
    list_filter = ('status',)

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status == 'shipped':
            obj.ship_order()
        super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)

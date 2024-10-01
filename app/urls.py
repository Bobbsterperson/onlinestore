from django.urls import path
from .views import store, add_to_cart, purchase, remove_from_cart

urlpatterns = [
    path('', store, name='store'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),  # New path
    path('purchase/', purchase, name='purchase'),
]

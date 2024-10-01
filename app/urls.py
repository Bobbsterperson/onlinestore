from django.urls import path
from .views import store, add_to_cart, purchase  # Import purchase view

urlpatterns = [
    path('', store, name='store'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('purchase/', purchase, name='purchase'),  # Add purchase URL
]

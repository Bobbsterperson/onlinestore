# urls.py
from django.urls import path
from .views import store, add_to_cart, remove_from_cart, purchase, register, logout_view

urlpatterns = [
    path('', store, name='store'),
    path('register/', register, name='register'),  # Add registration URL
    path('logout/', logout_view, name='logout'),  # Add logout URL
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('purchase/', purchase, name='purchase'),
]

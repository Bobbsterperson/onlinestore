from django.urls import path
from .views import store, add_to_cart

urlpatterns = [
    path('', store, name='store'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
]

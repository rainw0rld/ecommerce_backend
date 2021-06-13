from django.urls import path

from users.controllers.order_controller import OrderAPIView
from users.controllers.address_controller import AddressAPIView
from users.controllers.cart_controller import CartAPIView
from users.controllers.customer_controller import CustomerAPIView


urlpatterns = [
    path(r'orders/', OrderAPIView.as_view()),
    path(r'address/', AddressAPIView.as_view()),
    path(r'cart/', CartAPIView.as_view()),
    path(r'', CustomerAPIView.as_view())
]
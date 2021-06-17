from django.urls import path

from storefront.controllers.product_controller import BrandProductAPIView, CategoryProductAPIView
from storefront.controllers.product_detail_controller import ProductDetailAPIView

urlpatterns = [
    path(r'products/brand/<str:brand>', BrandProductAPIView.as_view()),
    path(r'products/category/<str:category>', CategoryProductAPIView.as_view()),
    path(r'product_detail/<str:id>', ProductDetailAPIView.as_view()),
]
from django.contrib import admin
from users.models import Address, Order, OrderItem, Customer
from storefront.models import Product, Category, Brand, ProductDetail, ProductAlbum


# Register your models here.


# admin.site.register(User)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(ProductDetail)
admin.site.register(ProductAlbum)
from rest_framework import serializers
from .models import Product, ProductDetail, Category, Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'brand', 'name', 'price', 'stock', 'discount', 'thumbnail']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'product']


class ProductDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductDetail
        exclude = ['viewcount']
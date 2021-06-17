from rest_framework import serializers
from .models import Product, ProductDetail, ProductAlbum, Category, Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'product']


class ProductAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAlbum
        fields = ['image']


class ProductDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    album = ProductAlbumSerializer(many=True, read_only=True)

    class Meta:
        model = ProductDetail
        exclude = ['viewcount']
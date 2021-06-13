from django.utils import timezone

from rest_framework import serializers

from .models import Address, Order, OrderItem, Customer

from storefront.models import Product
from storefront.serializers import ProductSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['user']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class EditCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['order']


class OrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    products = OrderItemSerializer(source='order_to_product', read_only=True, many=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(OrderSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Order
        fields = '__all__'


class PlaceOrderSerializer(serializers.ModelSerializer):
    payment_method = serializers.CharField(required=True)
    address_id = serializers.CharField(required=True)
    payment_method = serializers.CharField(default='success')
    time = serializers.DateTimeField(default=timezone.now)
    payment_status = serializers.CharField(default='received')

    class Meta:
        model = Order
        fields = ('id', 'payment_method', 'address_id', 'time', 'payment_status')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {"password": {"write_only": True}}

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(CustomerSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if instance:
            instance.set_password(password)
        instance.save()
        return instance

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models import Order, OrderItem
from users.serializers import EditCartItemSerializer, OrderSerializer


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Order.objects.get_or_create(user=request.user, status='cart')
        cart.set_price()
        serializer = OrderSerializer(cart, fields=('products', 'qty', 'total'))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cart = Order.cart.get_or_create(user=request.user)
        serializer = EditCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        item = OrderItem.objects.filter(order=cart, product_id=serializer.validated_data['product']).first()
        if item:
            serializer.validated_data['qty'] += item.qty
            serializer.instance = item

        serializer.save(order=cart)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        cart = Order.cart.get(user=request.user)
        item = OrderItem.objects.filter(product_id=request.data['product'], order=cart).first()
        if not item:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request):
        cart = Order.cart.get(user=request.user)
        item = OrderItem.objects.filter(product_id=request.data['product'], order=cart).first()
        if not item:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EditCartItemSerializer(item, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(status=status.HTTP_200_OK)
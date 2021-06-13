from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models import Order
from users.serializers import OrderSerializer, PlaceOrderSerializer


class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Order.orders.filter(user=request.user)
        if not queryset:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = OrderSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        cart = Order.cart.get(request.user)
        serializer = PlaceOrderSerializer(cart, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(status=status.HTTP_200_OK)
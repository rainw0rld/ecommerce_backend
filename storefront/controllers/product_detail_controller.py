from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from storefront.models import ProductDetail
from storefront.serializers import ProductDetailSerializer


class ProductDetailAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, id):
        product = ProductDetail.objects.get(id=id)
        serializer = ProductDetailSerializer(product)
        product.viewcount += 1
        product.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
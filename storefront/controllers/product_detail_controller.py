from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from storefront.models import ProductDetail
from storefront.serializers import ProductDetailSerializer


class ProductDetailAPIView(APIView):
    def get(self, request):
        product = ProductDetail.objects.get(id=request.data['product'])
        serializer = ProductDetailSerializer(product)
        product.viewcount += 1
        product.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
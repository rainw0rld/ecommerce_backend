from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from storefront.models import Product
from storefront.serializers import ProductSerializer


class ResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BrandProductAPIView(ListAPIView):
    authentication_classes = []

    serializer_class = ProductSerializer
    pagination_class = ResultsSetPagination
    lookup_url_kwarg = 'brand'

    def get_queryset(self):
        brand = self.kwargs.get('brand')
        products = Product.objects.filter(brand__name__icontains=brand)
        return products

class CategoryProductAPIView(ListAPIView):
    authentication_classes = []

    serializer_class = ProductSerializer
    pagination_class = ResultsSetPagination
    lookup_url_kwarg = 'category'

    def get_queryset(self):
        category = self.kwargs.get('category')
        products = Product.objects.filter(category__name__icontains=category)
        return products

class PopularProductAPIView(ListAPIView):
    pass





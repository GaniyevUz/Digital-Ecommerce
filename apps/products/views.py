from django_filters import rest_framework as filters
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from .models import Product, Category
from .serializers import ProductModelSerializer, CategoryModelSerializer, CategoryListSerializer


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    parser_classes = (MultiPartParser,)
    # filterset_fields = ('category',)
    filterset_fields = ('name', 'price')

    def get_queryset(self):
        qs = super().get_queryset()
        if shop := self.kwargs.get('shop'):
            return qs.filter(category__shop=shop)
        return qs


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if shop := self.kwargs.get('shop'):
            return qs.filter(shop=shop)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return super().get_serializer_class()

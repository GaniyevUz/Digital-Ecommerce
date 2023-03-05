from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response

from shared.django import APIViewSet

from shared.django import BaseShopMixin
from shared.restframework import CustomPageNumberPagination, IsShopOwner
from .models import Category, Product
from .serializers import (ProductModelSerializer, CategoryModelSerializer, CategoryListSerializer,
                          CategoryMoveSerializer)


class ProductAPIViewSet(BaseShopMixin, APIViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, IsShopOwner,)
    # parser_classes = (MultiPartParser,)
    # filterset_fields = ('category',)
    filterset_fields = ('name', 'price')
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return self.queryset.filter(category__shop=self.get_shop)


class CategoryAPIViewSet(BaseShopMixin, APIViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = IsShopOwner,

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return super().get_serializer_class()

    @action(['GET', 'PATCH'], True)
    def get_translations(self, request, shop, pk):
        try:
            ctg = self.get_queryset().get(shop=shop, pk=pk)
            return Response('ok')
        except Category.DoesNotExist:
            return Response(status=404)

    @action(['GET', 'PATCH'], True, serializer_class=CategoryMoveSerializer)
    def move(self, *args, **kwargs):
        return Response('move')

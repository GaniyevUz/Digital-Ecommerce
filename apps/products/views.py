from django_filters import rest_framework as filters
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.mixins import BaseShopMixin
from shared.paginate import CustomPageNumberPagination
from shared.permisions import IsShopOwner
from .models import Category, Product
from .serializers import (ProductModelSerializer, CategoryModelSerializer, CategoryListSerializer,
                          CategoryMoveSerializer)


class ProductModelViewSet(BaseShopMixin, ModelViewSet):
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


class CategoryModelViewSet(BaseShopMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = IsShopOwner,

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return super().get_serializer_class()


class ProductCategoryMoveAPI(GenericAPIView):
    serializer_class = CategoryMoveSerializer
    queryset = Product.objects.all()

    def post(self, request, shop, pk):  # TODO to finish
        Category.objects.filter(shop=shop, pk=pk)
        print(123)
        print(123)
        # CategoryMoveSerializer()
        # self.get_object()
        # category = self.get_queryset().get(pk=pk)
        # category.move_to()
        return Response({'position': 3})

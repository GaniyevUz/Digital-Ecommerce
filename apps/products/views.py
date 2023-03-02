from django_filters import rest_framework as filters
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ModelViewSet

from shared.django import BaseShopMixin
from shared.restframework import CustomPageNumberPagination, IsShopOwner
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

    # def generate_category(self, shop, pk):
    #     # category.move_to(Category.objects.get(pk=15))
    #     print(17)
    #     # c1 = Category.objects.create(
    #     #     name={'uz': "Ko'chmas mulk"},
    #     #     shop_id=shop
    #     # )
    #     # c11 = Category.objects.create(
    #     #     name={'uz': "Sutkalik ijarasi'"},
    #     #     shop_id=shop,
    #     #     parent=c1
    #     # )
    #     # c12 = Category.objects.create(
    #     #     name={'uz': "Kvartiralar'"},
    #     #     shop_id=shop,
    #     #     parent=c1
    #     # )
    #     #
    #     # c2 = Category.objects.create(
    #     #     name={'uz': "Transport"},
    #     #     shop_id=shop,
    #     # )
    #     #
    #     # c21 = Category.objects.create(
    #     #     name={'uz': "Yengil avtomashinalar"},
    #     #     shop_id=shop,
    #     #     parent=c2
    #     # )
    #     #
    #     # c22 = Category.objects.create(
    #     #     name={'uz': "Avto ehtiyot qismlari va aksessuarlar"},
    #     #     shop_id=shop,
    #     #     parent=c2
    #     # )
    #     #
    #     # c23 = Category.objects.create(
    #     #     name={'uz': "Shinalar, disklar va g'ildiraklar"},
    #     #     shop_id=shop,
    #     #     parent=c2
    #     # )
    #
    # def post(self, request, shop, pk):
    #     position = request.data.get('position')
    #     if position:
    #         category = get_object_or_404(Category, pk=pk, shop_id=shop)
    #         move_category = Category.objects.filter(pk=position, shop_id=shop, tree_id=category.tree_id).first()  # noqa
    #         category.move_to(move_category, 'left')
    #         # self.generate_category(shop, pk)
    #         return Response({'position': position})

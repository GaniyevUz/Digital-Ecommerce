from django_filters import rest_framework as filters
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from shared.mixins import CountResultMixin
from shared.paginate import Page20NumberPagination
from shared.permisions import IsShopOwner
from shops.models import Shop
from shared.mixins import ShopRequiredMixin
from .models import Product, Category
from .serializers import ProductModelSerializer, CategoryModelSerializer, CategoryListSerializer


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    pagination_class = Page20NumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsShopOwner,)
    # parser_classes = (MultiPartParser,)
    # filterset_fields = ('category',)
    filterset_fields = ('name', 'price')

    def get_queryset(self):
        return get_object_or_404(Shop, pk=self.kwargs.get('shop')).products


class CategoryModelViewSet(ModelViewSet, ShopRequiredMixin,  CountResultMixin):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

    def list(self, request, *args, **kwargs):
        return self.count_result_list(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        if shop := self.kwargs.get('shop'):
            return qs.filter(shop=shop)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return super().get_serializer_class()

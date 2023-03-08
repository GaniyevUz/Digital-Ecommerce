from django.http import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.django import APIViewSet
from shared.django import BaseShopMixin
from shared.django.mixins import ImportExportMixin
from shared.restframework import CustomPageNumberPagination, IsShopOwner
from .models import Category, Product
from .serializers import (ProductModelSerializer, CategoryModelSerializer, CategoryListSerializer,
                          CategoryMoveSerializer, CategoryTranslationSerializer)


class ProductAPIViewSet(BaseShopMixin, APIViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsShopOwner,)
    # parser_classes = (MultiPartParser,)
    # filterset_fields = ('category',)
    filterset_fields = ('name', 'price')
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return self.queryset.filter(category__shop=self.get_shop)


class ExportProductAPI(BaseShopMixin, ImportExportMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = ()

    def get_queryset(self):
        return self.queryset.filter(category__shop=self.get_shop)  # noqa

    def get(self, request, *args, **kwargs):
        fields = ('pk', 'name', 'description', 'category', 'price', 'in_availability',
                  'length', 'width', 'height', 'weight', 'length_class', 'weight_class')
        products = self.export(*fields)
        shop = self.get_shop
        response = HttpResponse(products, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'filename={shop}.xlsx;'.format(shop=shop)
        return response


class CategoryAPIViewSet(BaseShopMixin, APIViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = IsShopOwner,

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return super().get_serializer_class()


class CategoryMoveAPI(GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryMoveSerializer

    def post(self, request, shop, pk, *args, **kwargs):
        categories = self.get_queryset().filter(shop=shop)
        not_found = 'No matching Category given %s'
        if categories:
            target = request.data.get('position')
            if target is not None and target in categories.values_list('pk', flat=True):
                try:
                    target = categories.get(pk=target)
                except Category.DoesNotExist:
                    return Response({'status': not_found % 'position'}, status.HTTP_404_NOT_FOUND)
                try:
                    category: Category = categories.get(pk=pk)
                    category.move_to(target, 'left')
                    data = {'position': category.pk}
                    return Response(data)
                except Category.DoesNotExist:
                    return Response({'status': not_found % 'id'}, status.HTTP_404_NOT_FOUND)
            else:
                return Response({'status': 'Invalid Request'}, status.HTTP_400_BAD_REQUEST)
        return Response({'status': not_found % 'shop_id'}, status.HTTP_400_BAD_REQUEST)


class CategoryTranslationsAPI(GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryTranslationSerializer

    def get(self, request, shop, pk, *args, **kwargs):
        try:
            category = Category.objects.get(shop=shop, pk=pk)
            serializer = self.get_serializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({'status': 'Category Not Found'}, status.HTTP_404_NOT_FOUND)

    def patch(self, request, shop, pk, *args, **kwargs):
        try:
            category = Category.objects.get(shop=shop, pk=pk)
            serializer = self.get_serializer(category, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({'status': 'Category Not Found'}, status.HTTP_404_NOT_FOUND)

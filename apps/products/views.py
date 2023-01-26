from rest_framework.viewsets import ModelViewSet

from shops.models import Category
from .models import Product
from .serializers import ProductModelSerializer, CategoryModelSerializer


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()

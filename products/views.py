from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ViewSetMixin, ModelViewSet

from .models import Product, Category
from .serializers import ProductModelSerializer, CategoryModelSerializer


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()

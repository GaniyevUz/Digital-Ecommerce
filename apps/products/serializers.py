from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from products.models import Product
from shops.models import Category


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

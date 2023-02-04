from rest_framework.serializers import ModelSerializer

from products.models import Product, Category


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = 'rght', 'lft', 'tree_id', 'level'


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

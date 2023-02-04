from rest_framework.serializers import ModelSerializer

from products.models import Product, Category


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = 'lft', 'rght', 'level', 'tree_id', 'shop'

    def create(self, validated_data):
        return super().create(validated_data)


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

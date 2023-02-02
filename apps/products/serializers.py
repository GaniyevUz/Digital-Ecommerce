from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from rest_framework.serializers import ModelSerializer

from products.models import Product, Category


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

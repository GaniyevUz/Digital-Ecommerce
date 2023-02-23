import pytest

from products.models import Product, Category
from products.serializers import ProductModelSerializer
from products.tests.fixture import FixtureClass


@pytest.mark.django_db
class TestProductModelSerializer(FixtureClass):
    def test_product_model_serializer(self, create_category):
        category = Category.objects.first()
        expected_data = {
            'id': 1,
            'name': 'name',
            'category': category,
            'description': 'description',
            'image': None,
            'price': '5600',
            'in_availability': True,
            'length': None,
            'width': None,
            'height': None,
            'weight': None,
            'length_class': None,
            'weight_class': None,
            'attributes': [{}],
        }

        product = Product(**expected_data)
        expected_data['category'] = category.pk
        result = ProductModelSerializer(product).data

        assert result == expected_data

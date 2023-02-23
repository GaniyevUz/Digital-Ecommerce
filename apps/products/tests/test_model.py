import pytest

from products.models import Category as PrCategory, Product
from products.tests.fixture import FixtureClass
from shops.models import Shop, Category as ShCategory


@pytest.mark.django_db
class TestProductManager(FixtureClass):

    def test_get_products_by_created(self, create_products):
        shop_category_count = ShCategory.objects.count()
        ShCategory.objects.create(name='shop category')

        product_category_count = PrCategory.objects.count()
        category = PrCategory.objects.create(name='pr category',
                                             description='descr',
                                             shop=Shop.objects.first())

        product_count = Product.objects.count()
        Product.objects.create(
            name='new product',
            description='desc',
            category=category,
            price=5600,
            attributes=[{}],
        )

        assert ShCategory.objects.count() - 1 == shop_category_count
        assert PrCategory.objects.count() - 1 == product_category_count
        assert Product.objects.count() - 1 == product_count

import pytest

from shops.models import ShopCategory, ShopCurrency


@pytest.mark.django_db
class TestShopRelatedModels:
    @pytest.fixture
    def shop_related_models(self):
        ShopCategory.objects.create(name='Category 1')
        ShopCurrency.objects.create(name='UZS')

    def test_create_model(self, shop_related_models):
        name = 'Name'
        count = ShopCategory.objects.count()
        category = ShopCategory.objects.create(name=name)
        assert category.name == name
        assert ShopCategory.objects.count() - 1 == count
        assert ShopCurrency.objects.count() == 1
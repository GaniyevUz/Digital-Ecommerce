import pytest

from shops.models import Category, Currency


@pytest.mark.django_db
class TestShopRelatedModels:
    @pytest.fixture
    def shop_related_models(self):
        category = Category.objects.create(name='Category 1')
        currency = Currency.objects.create(name='Currency 1')
        assert str(category) == category.name
        assert str(currency) == currency.name

    def test_create_model(self, shop_related_models):
        name = 'Name'
        category = Category.objects.create(name=name)
        assert category.name == name
        assert Category.objects.count() == 2

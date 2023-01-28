import pytest

from shops.models import ShopCategory


@pytest.mark.django_db
class TestShopRelatedModels:
    @pytest.fixture
    def shop_related_models(self):
        ShopCategory.objects.create(name='Category 1')

    def test_create_model(self, shop_related_models):
        name = 'Name'
        category = ShopCategory.objects.create(name=name)
        assert category.name == name
        assert ShopCategory.objects.count() == 2

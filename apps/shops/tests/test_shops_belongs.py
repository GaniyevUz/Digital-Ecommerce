import pytest

from shops.models import Category


@pytest.mark.django_db
class TestShopRelatedModels:
    @pytest.fixture
    def shop_related_models(self):
        Category.objects.create(name='Category 1')

    def test_create_model(self, shop_related_models):
        name = 'Name'
        category = Category.objects.create(name=name)
        assert category.name == name
        assert Category.objects.count() == 2

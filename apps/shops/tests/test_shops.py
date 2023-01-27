from random import randint

import pytest
from django.contrib.auth.hashers import make_password
from faker import Faker

from shops.models import Shop, ShopCategory, ShopCurrency
from users.models import User

fake = Faker()
Faker.seed(0)


@pytest.mark.django_db
class TestShopAPIView:
    @pytest.fixture
    def create_shop_models(self):
        for _ in range(20):
            ShopCategory.objects.create(name=fake.first_name())
            ShopCurrency.objects.create(name=fake.currency_code())
        else:
            Shop.objects.create(name=fake.name(), shop_category_id=randint(1, 10), shop_currency_id=randint(1, 10),
                                user_id=1,
                                languages=['uz', 'en', 'ru'],
                                )
            User.objects.create(username='user 1', password=make_password('1234'))

    def test_create_model(self, create_shop_models):
        for i in range(20):
            Shop.objects.create(
                name=fake.name(),
                shop_category_id=randint(1, 20),
                shop_currency_id=randint(1, 20),
                languages=['uz', 'en', 'ru'],
                user_id=1
            )
        assert Shop.objects.count() == 21
        assert ShopCategory.objects.count() == 20
        assert ShopCurrency.objects.count() == 20

    def test_get_user_shops_api(self, client):
        pass
